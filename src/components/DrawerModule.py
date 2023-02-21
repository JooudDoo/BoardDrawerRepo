
import cv2
import numpy as np

from components.ColorContainers import ColorContainer, RGB, HSL
from components.CameraHandler import CameraHandler

class Drawer():

    def __init__(self, camera : CameraHandler, defaultColor : RGB = RGB(0, 255, 255)):
        self.camera = camera
        self._draw : bool = False
        self._showMask : bool = False

        self.defaultColor = defaultColor
        self._save_x = 0
        self._save_y = 0
        self._drawCanvas = Drawer.createCanvas(self.camera.getFrame())
    
    def swictchMaskShowMode(self):
        self._showMask = not self._showMask
        return self._showMask

    # при смене состояния обновлять параметры рисовальщика (обрыв линии...)
    def switchDrawMode(self):
        self._draw = not self._draw
        self._save_x = 0
        self._save_y = 0
        return self._draw

    def drawer(self, size : tuple [int, int] = (0,0)):
        frame = self.camera.getFrame(size)
        mask = self.camera.getColorRangeMask(frame)
        resultMask = self._drawCanvas
        if self._draw:
            resultMask = self.getMoments(frame, mask)
        if self._showMask:
            resultMask = cv2.add(resultMask, cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR))
        return self.applyMask(frame, resultMask)

    # переписать возможна смена размеров входного изображения
    @staticmethod
    def createCanvas(img):
        h, w = img.shape[:2]
        return np.zeros((h, w, 3), np.uint8)

    def cleanCanvas(self):
        self._drawCanvas = np.zeros_like(self._drawCanvas)

    def applyMask(self, img, mask, alpha : float = 0.6, gamma : float = 0.1):
        beta = 1 - alpha
        return cv2.addWeighted(img, alpha, mask, beta, gamma)

    # Переписать и разделить на под функции
    def getMoments(self, img, mask):
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
                cv2.line(self._drawCanvas, (self._save_x, self._save_y), (x, y), self.defaultColor.color, 5)

        self._save_x = x
        self._save_y = y

        return self._drawCanvas
        # cv2.add(img, self._drawCanvas)
