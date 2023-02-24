from dataclasses import dataclass

import cv2
import numpy as np
from imutils.video import VideoStream

from components.ColorContainers import ColorContainer, RGB, HSL

@dataclass
class CameraSettings():
    """
    dataclass содержащий настройки камеры

    Parametrs
    ---------
    `minRange` - Минимальные значение RGB для обнаружения их на видео потоке

    `maxRange` - Максимальные значения RGB для обнаружения их на видео потоке
    """

    @staticmethod
    def default():
        return CameraSettings(rangeType="RGB", minRange=(0,0,0), maxRange=(255,255,255))

    rangeType : str
    minRange : ColorContainer
    maxRange : ColorContainer
    maskReduceBy : int 

    @staticmethod
    def importFrom(fileName : str):
        with open(fileName, 'r', encoding='utf8') as importFile:
            type = importFile.readline().strip()
            if type == "RGB":
                minRange = RGB(rgb=[int(x) for x in importFile.readline().split()])
                maxRange = RGB(rgb=[int(x) for x in importFile.readline().split()])
            elif type == "HSL":
                minRange = HSL(hsl=[int(x) for x in importFile.readline().split()])
                maxRange = HSL(hsl=[int(x) for x in importFile.readline().split()])
            maskReduceBy = int(importFile.readline())
        try:
            settings = CameraSettings(
                    rangeType=type,
                    minRange=minRange,
                    maxRange=maxRange,
                    maskReduceBy=maskReduceBy)
        except:
            settings = CameraSettings.default()
        return settings

    @staticmethod
    def exportTo(settings, fileName : str):
        with open(fileName, 'w', encoding='utf8') as exportFile:
            exportFile.write(f"{settings.rangeType}\n")
            [exportFile.write(f"{x} ") for x in settings.minRange.color]
            exportFile.write('\n')
            [exportFile.write(f"{x} ") for x in settings.maxRange.color]
            exportFile.write('\n')
            exportFile.write(f"{settings.maskReduceBy}\n")

class CameraHandler():

    def __init__(self, videoStreamSource = 0, settings : CameraSettings | str = None):
        self._videoStream = VideoStream(src=videoStreamSource).start()
        if type(settings) == str:
            self.loadSettings(settings)
        else:
            self.setupSettings(settings)
    
    def setupSettings(self, settings : CameraSettings):
        if settings == None:
            self.settings = None
            return
        else:
            # Тут возможно будет верификация настроек
            self.settings = settings
    
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

    def getFrame(self, size : tuple[int, int] = (0, 0)):
        frame = self._videoStream.read()
        #if not checkCode:
        #    raise Exception("Frame not received")
        if size != (0, 0):
            frame = cv2.resize(frame, size)
        return frame

    def getMaskedFrame(self, size : tuple[int, int] = (0, 0)):
        frame = self.getFrame(size)
        mask = self.getColorRangeMask(frame)
        maskedFrame = self.applyMaskOnImage(frame, mask)
        return maskedFrame

    def getColorRangeMask(self, img : cv2.Mat, reduceBy : int = None) -> cv2.Mat:
        """
        Функция возвращающая маску заданного цветового диапазона. Значение маски берется из настроек

        Parametrs
        ---------
        `img` - изображение, с которого снимается маска

        `reduceBy` - коэффицент сжатия картинки по обоим осям

        `return` - маска изображения
        """
        if reduceBy == None:
            reduceBy = self.settings.maskReduceBy
        h, w, _ = img.shape
        imgCopy = cv2.resize(img, (w//reduceBy, h//reduceBy))
        if self.settings.rangeType == "HSL":
            imgCopy = cv2.cvtColor(imgCopy, cv2.COLOR_BGR2HLS)
        imgCopy = cv2.GaussianBlur(imgCopy, (5, 5), 0)
        mask = cv2.inRange(imgCopy, self.settings.minRange.color, self.settings.maxRange.color)
        mask = cv2.dilate(mask, np.ones((2,2)), iterations=3)
        mask = cv2.resize(mask, (w,h))
        return mask

    @staticmethod
    def applyMaskOnImage(img : cv2.Mat, mask : cv2.Mat, alpha : float = 0.6, gamma : float = 0.1) -> cv2.Mat:
        beta = 1 - alpha
        mask = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
        return cv2.addWeighted(img, alpha, mask, beta, gamma)

    def __del__(self):
        self._videoStream.stop()