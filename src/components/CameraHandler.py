from dataclasses import dataclass
from contextlib import suppress

import cv2
import numpy as np

class ColorContainer():
    def __init__():
        pass

@dataclass
class RGB(ColorContainer):
    """
    Класс содержащий значения RGB
    """
    name : str = "RGB"
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
        with suppress (RecursionError): self.color = (self.red, self.green, self.blue)
        
    def __str__(self):
        return f"[R: {self.red}, G: {self.green}, B: {self.blue}]"
    
    def maximizedString(self):
        return f"[R: 255, G: 255, B: 255]"

@dataclass
class HSL(ColorContainer):
    """
    Класс содержащий значения HLS
    """
    name : str = "HSL"
    hue : int = 0
    saturation : int = 0
    lightness : int = 0

    def __init__(self, hue = 0, saturation = 0, lightness = 0, hsl = ()):
        if hsl:
            self.hue, self.saturation, self.lightness = hsl[0], hsl[1], hsl[2]
        else:
            self.hue, self.saturation, self.lightness = hue, saturation, lightness
    
    def _updateColorByName(self, color : str, val):
        setattr(self, color, val)

    def __setattr__(self, name, val):
        """
        Обновляет поле в классе, а также сохрянет достоверность массива 'rgb'
        """
        object.__setattr__(self, name, val)
        with suppress (RecursionError): self.color = (self.hue, self.saturation, self.lightness)
        
    def __str__(self):
        return f"[H: {self.hue}, S: {self.saturation}, L: {self.lightness}]"
    
    def maximizedString(self):
        return f"[H: 255, S: 255, L: 255]"
        
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
        try:
            settings = CameraSettings(
                    rangeType=type,
                    minRange=minRange,
                    maxRange=maxRange,)
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

class CameraHandler():

    def __init__(self, videoStreamSource = 0, settings : CameraSettings = None):
        self._videoStream = cv2.VideoCapture(videoStreamSource)
        self.setupSettings(settings)


        # ----- Настройки цветов ВРЕМЕННОЕ
        self.circle_color = (0,0,0)
        self.line_color = (0, 255, 255)
        self.save_x = 0
        self.save_y = 0
        self.path = CameraHandler.createPath(self.getImage())
    
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
        rangedImage = self.getMoments(frame, mask)
        maskedImage = self.applyMaskOnImage(frame, mask)
        return cv2.add(maskedImage, rangedImage)

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
        if self.settings.rangeType == "HSL":
            imgCopy = cv2.cvtColor(imgCopy, cv2.COLOR_BGR2HLS)
        imgCopy = cv2.GaussianBlur(imgCopy, (5, 5), 0)
        mask = cv2.inRange(imgCopy, self.settings.minRange.color, self.settings.maxRange.color)
        mask = cv2.dilate(mask, np.ones((2,2)), iterations=3)
        mask = cv2.resize(mask, (w,h))
        return mask

    def applyMaskOnImage(self, img : cv2.Mat, mask : cv2.Mat, alpha : float = 0.6, gamma : float = 0.1) -> cv2.Mat:
        beta = 1 - alpha
        mask = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
        return cv2.addWeighted(img, alpha, mask, beta, gamma)

    def __del__(self):
        self._videoStream.release()


    # РИСОВКА ВРЕМЕННОЕ ----
    @staticmethod
    def createPath(img):
        h, w = img.shape[:2]
        return np.zeros((h, w, 3), np.uint8)

    def getMoments(self, img, thresh):
        moments = cv2.moments(thresh, 1)
        dM01 = moments['m01']
        dM10 = moments['m10']
        dArea = moments['m00']

        x = 0
        y = 0
        if dArea > 10:
            x = int(dM10 / dArea)
            y = int(dM01 / dArea)
            
        if self.save_x > 0 and self.save_y > 0 and x > 0 and y > 0:
            cv2.line(self.path, (self.save_x, self.save_y), (x, y), self.line_color, 5)

        self.save_x = x
        self.save_y = y

        return cv2.add(img, self.path)
