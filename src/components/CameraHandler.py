from dataclasses import dataclass
from contextlib import suppress
from typing import Dict

import cv2
import numpy as np

@dataclass
class RGB():
    """
    Класс содержащий значения RGB
    """
    red : int = 0
    green : int = 0
    blue : int = 0

    def __init__(self, red = 0, green = 0, blue = 0, rgb = ()):
        if rgb:
            self.red, self.green, self.blue = rgb[0], rgb[1], rgb[2]
        else:
            self.red, self.green, self.blue = red, green, blue
    
    def _updateColorByName(self, color : str, val):
        setattr(self, color, val)

    def __setattr__(self, name, val):
        """
        Обновляет поле в классе, а также сохрянет достоверность массива 'rgb'
        """
        object.__setattr__(self, name, val)
        with suppress (RecursionError): self.rgb = (self.red, self.green, self.blue)
        
    def __str__(self):
        return f"[R: {self.red}, G: {self.green}, B: {self.blue}]"
    
    def maximizedString(self):
        return f"[R: 255, G: 255, B: 255]"
        
@dataclass
class CameraSettings():
    """
    dataclass содержащий настройки камеры

    Parametrs
    ---------
    `minRangeRGB` - Минимальные значение RGB для обнаружения их на видео потоке

    `maxRangeRGB` - Максимальные значения RGB для обнаружения их на видео потоке
    """
    minRangeRGB : RGB
    maxRangeRGB : RGB

    @staticmethod
    def importFrom(fileName : str):
        with open(fileName, 'r', encoding='utf8') as importFile:
            minRange = RGB(rgb=[int(x) for x in importFile.readline().split()])
            maxRange = RGB(rgb=[int(x) for x in importFile.readline().split()])

        settings = CameraSettings(minRangeRGB=minRange,
                                    maxRangeRGB=maxRange)
        return settings

    @staticmethod
    def exportTo(settings, fileName : str):
        with open(fileName, 'w', encoding='utf8') as exportFile:
            [exportFile.write(f"{x} ") for x in settings.minRangeRGB.rgb]
            exportFile.write('\n')
            [exportFile.write(f"{x} ") for x in settings.maxRangeRGB.rgb]

class CameraHandler():

    def __init__(self, videoStreamSource = 0, settings : CameraSettings = None):
        self._videoStream = cv2.VideoCapture(videoStreamSource)
        self.setupSettings(settings)
    
    def setupSettings(self, settings : CameraSettings):
        if settings == None:
            self._settings = None
            return
        else:
            # Тут возможно будет верификация настроек
            self._settings = settings
    
    def loadSettings(self, fileName):
        """
        WIP
        -----
        Загружает настройки из файла

        Parametrs
        ---------
        `fileName` - имя файла с настройками
        """
        self.setupSettings(CameraSettings.importFrom(fileName))

    @property
    def settings(self):
        return self._settings

    def getImage(self, size : tuple[int, int] = (0, 0)):
        checkCode, frame = self._videoStream.read()
        if not checkCode:
            raise Exception("Frame not received")
        if size != (0, 0):
            frame = cv2.resize(frame, size)
        return frame

    def getProcessedImage(self, size : tuple[int, int] = (0, 0)):
        frame = self.getImage(size)
        mask = self.getColorRangeMask(frame)
        rangedImage = self.applyMaskOnImage(frame, mask)
        return rangedImage

    def getColorRangeMask(self, img : cv2.Mat, reduceBy : int = 5) -> cv2.Mat:
        """
        Функция возвращающая маску заданного цветового диапазона. Значение маски берется из настроек

        Parametrs
        ---------
        `img` - изображение, с которого снимается маска

        `reduceBy` - коэффицент сжатия картинки по обоим осям

        `return` - маска изображения
        """
        h, w, _ = img.shape
        imgCopy = cv2.resize(img, (w//reduceBy, h//reduceBy))
        imgCopy = cv2.GaussianBlur(imgCopy, (5, 5), 0)
        mask = cv2.inRange(imgCopy, self.settings.minRangeRGB.rgb, self.settings.maxRangeRGB.rgb)
        mask = cv2.dilate(mask, np.ones((2,2)), iterations=3)
        mask = cv2.resize(mask, (w,h))
        return mask

    def applyMaskOnImage(self, img : cv2.Mat, mask : cv2.Mat, alpha : float = 0.6, gamma : float = 0.1) -> cv2.Mat:
        beta = 1 - alpha
        mask = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
        return cv2.addWeighted(img, alpha, mask, beta, gamma)

    def __del__(self):
        self._videoStream.release()
