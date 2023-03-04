
from typing import Callable
from enum import Enum

import cv2
import numpy as np

from components.ColorContainers import RGB
from components.CameraHandler import CameraHandler


class Layer(Enum):
    """
    Enum содержащий имя слоев

    Значением Enum'а должна быть строка содержащая имя переменной, которая будет передаватся в функции сборщики
    """

    image = "image"
    laserMask = "laserMask"
    drawCanvas = "drawCanvas"


class LayerInfo():
    """
    Класс содержащий основную информацию для генерации нового слоя

    Параметры
    ---------
    `layer` - имя целевого слоя

    `func` - функция для сборки слоя

    `dependsOn` - список слоев необходимых для сборки целевого слоя
    """
    def __init__(self, layer: Layer, func: Callable, dependsOn: list[Layer] = []):
        self.layer = layer
        self._func = func
        self.func = self.funcWrapper
        self.dependsOn = dependsOn

    def funcWrapper(self, layers: dict[Layer, cv2.Mat]) -> cv2.Mat:
        deps: dict[Layer, cv2.Mat] = dict()
        for depend in self.dependsOn:
            deps.update({depend.value: layers.get(depend)})
        return self._func(**deps)


class BasicImageProcessor():
    """
    Базовый класс обработчика изображений
    -------
    """

    def __init__(self, camera: CameraHandler):
        self.cameraHandler = camera
        self.layersInfo: dict[Layer, LayerInfo] = dict()

    def addLayerInfo(self, layerInfo: LayerInfo):
        """
        Добавление описания слоя для системы сборки зависимостей слоев

        Параметры
        ---------
        `layerInfo` - класс с описанием генерации слоя
        """
        self.layersInfo.update({layerInfo.layer: layerInfo})

    def _getLayerInfo(self, layer: Layer):
        return self.layersInfo.get(layer)

    def _createLayerDepends(self, layer: Layer, depsIn: dict[Layer, cv2.Mat] = dict()):
        """
        Создание необходимых зависимостей для создания целевого слоя

        Параметры
        ---------
        `layer` - ключевой слой

        `depsIn` - словарь с сгенерированными зависимостями
        """
        deps: dict[Layer, cv2.Mat] = depsIn
        for depend in self._getLayerInfo(layer).dependsOn:
            if depend not in deps:
                if self._getLayerInfo(depend).dependsOn == []:
                    deps.update({depend: self._getLayerInfo(depend).func(deps)})
                else:
                    deps = self._createLayerDepends(depend, deps)
                    deps.update({depend: self._getLayerInfo(depend).func(deps)})
        return deps

    def __call__(self, layers: list[Layer]):
        return self._getLayers(layers)

    def _getLayers(self, layers: list[Layer]):
        """
        Создание слоев по запросу. Производит сборку зависимостей.

        Параметры
        ---------
        `layers` - список содержащий слои запрашиваемые для сборки
        """
        imageLayers: dict[Layer, cv2.Mat] = dict()
        deps: dict[Layer, cv2.Mat] = dict()
        for layer in layers:
            try:
                deps = self._createLayerDepends(layer, deps)
            except (AttributeError, TypeError) as atr:
                print(f"It is not possible to collect layer dependencies: {atr}")

        for layer in layers:
            try:
                if layer in deps:
                    imageLayers.update({layer: deps[layer]})
                else:
                    imageLayers.update(
                        {layer: self._getLayerInfo(layer).func(deps)})
            except (AttributeError, TypeError) as atr:
                print(f"Unable to assemble layer, function error: {atr}")

        return imageLayers

    def setCameraHandler(self, camera: CameraHandler):
        self.cameraHandler = camera

    @property
    def cameraAttached(self):
        return not self.cameraHandler is None


class DebugImageProcessor(BasicImageProcessor):

    def __init__(self, *args, **kwrgs):
        super().__init__(*args, **kwrgs)
        self.setupLayers()

        self.defaultColor = RGB(0, 255, 255)
        self._draw = False
        self._save_x = 0
        self._save_y = 0
        if self.cameraAttached:
            self._drawCanvas = self.createCanvas(self.cameraHandler.getFrame())

    def createCanvas(self, img: cv2.Mat):
        h, w = img.shape[:2]
        return np.zeros((h, w, 3), np.uint8)

    def cleanCanvas(self):
        self._drawCanvas = np.zeros_like(self._drawCanvas)

    def setupLayers(self):
        self.addLayerInfo(LayerInfo(Layer.image, self.cameraHandler.getFrame))
        self.addLayerInfo(LayerInfo(Layer.laserMask, self.cameraHandler.getColorRangeMask, [Layer.image]))
        self.addLayerInfo(LayerInfo(Layer.drawCanvas, self.getMoments, [Layer.laserMask]))

    def switchDrawMode(self):
        self._draw = not self._draw
        self._save_x = 0
        self._save_y = 0
        return self._draw

    def getMoments(self, laserMask: cv2.Mat):
        mask = cv2.cvtColor(laserMask, cv2.COLOR_BGR2GRAY)
        if not self._draw:
            return self._drawCanvas
        moments = cv2.moments(mask, 1)
        dM01 = moments['m01']
        dM10 = moments['m10']
        dArea = moments['m00']

        x = 0
        y = 0
        if dArea > 100:
            x = int(dM10 / dArea)
            y = int(dM01 / dArea)

            if self._save_x > 0 and self._save_y > 0 and x > 0 and y > 0:
                cv2.line(self._drawCanvas, (self._save_x, self._save_y),
                         (x, y), self.defaultColor.color, 5)

        self._save_x = x
        self._save_y = y

        return self._drawCanvas
        
    

def applyMask(img, mask, weighted: bool = False, alpha: float = 0.6, gamma: float = 0.1):
    if not weighted:
        return cv2.add(img, mask)
    beta = 1 - alpha
    return cv2.addWeighted(img, alpha, mask, beta, gamma)


def createImageFromLayers(layers: dict[Layer, cv2.Mat], Layer: list[Layer]) -> cv2.Mat:
    resultImage = None
    for filter in Layer:
        resultImage = applyFilter(resultImage, layers[filter])
    return resultImage


def applyFilter(img, layer):
    if img is None:
        return layer
    else:
        return applyMask(img, layer)
