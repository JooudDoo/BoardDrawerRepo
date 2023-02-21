
import cv2
import numpy as np

from components.ColorContainers import ColorContainer, RGB, HSL
from components.CameraHandler import CameraHandler

class Drawer():

    def __init__(self, camera : CameraHandler, reduceScale = 3, defaultColor : RGB = RGB(0, 255, 255)):
        self.camera = camera
        self._reduceScale = reduceScale
        self._draw : bool = False

        self.defaultColor = defaultColor
        self._save_x = 0
        self._save_y = 0
        self._drawCanvas = Drawer.createCanvas(self.camera.getFrame())
    
    # при смене состояния обновлять параметры рисовальщика (обрыв линии...)
    def switchMode(self):
        self._draw = not self._draw
        return self._draw

    def drawer(self, size : tuple [int, int] = (0,0)):
        frame = self.camera.getFrame(size)
        mask = self.camera.getColorRangeMask(frame, reduceBy=self._reduceScale)
        if self._draw :
            return self.getMoments(frame, mask)
        return self.applyCanvas(frame)

    # переписать возможна смена размеров входного изображения
    @staticmethod
    def createCanvas(img):
        h, w = img.shape[:2]
        return np.zeros((h, w, 3), np.uint8)

    def cleanCanvas(self):
        self._drawCanvas = np.zeros_like(self._drawCanvas)

    def applyCanvas(self, img, alpha : float = 0.6, gamma : float = 0.1):
        beta = 1 - alpha
        return cv2.addWeighted(img, alpha, self._drawCanvas, beta, gamma)

    # Переписать и разделить на под функции
    def getMoments(self, img, mask):
        moments = cv2.moments(mask, 1)
        dM01 = moments['m01']
        dM10 = moments['m10']
        dArea = moments['m00']

        x = 0
        y = 0
        if dArea > 10:
            x = int(dM10 / dArea)
            y = int(dM01 / dArea)
            
        if self._save_x > 0 and self._save_y > 0 and x > 0 and y > 0:
            cv2.line(self._drawCanvas, (self._save_x, self._save_y), (x, y), self.defaultColor.color, 5)

        self._save_x = x
        self._save_y = y

        return self.applyCanvas(img)
        # cv2.add(img, self._drawCanvas)
