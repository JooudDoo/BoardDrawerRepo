import numpy as np

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QAction

class FPSMeter(QtWidgets.QLabel):
    def __init__(self,  *args, **kwargs):
        super(FPSMeter, self).__init__( *args, **kwargs)
        self.paddingLeft = 5
        self.paddingTop = 5
        self.setText("")
    
    def updatePosition(self):
        if hasattr(self.parent(), 'viewport'):
            parentRect = self.parent().viewport().rect()
        else:
            parentRect = self.parent().rect()
        if not parentRect: return

        x = parentRect.width() - self.width() - self.paddingLeft
        y = self.paddingTop
        self.setGeometry(x, y, self.width(), self.height())
    
    def resizeEvent(self, a0: QtGui.QResizeEvent) -> None:
        super().resizeEvent(a0)
        self.updatePosition()

class ImageViewer(QtWidgets.QLabel):
    # Переделать логику ресайза
    def __init__(self,  *args, **kwargs):
        super(ImageViewer, self).__init__(*args, **kwargs)
        self.setText("default")
        try:
            self.defaultImage = QtGui.QPixmap("assets/defaultImage.jpg")
        except:
            self.defaultImage = np.zeros((360, 360, 3))
        self.setPixmap(self.defaultImage)
        self.FPSMeter = FPSMeter(parent=self)
        
    def setFPSMeterFPS(self, fps : float):
        self.FPSMeter.setText(f"FPS: {round(fps, 2)}")

    def setPixmap(self, pixmap):
        super(ImageViewer, self).setPixmap(pixmap.scaled(
            self.width()-25, self.height()-20,
            QtCore.Qt.KeepAspectRatio))
    
    def resizeEvent(self, a0: QtGui.QResizeEvent) -> None:
        super().resizeEvent(a0)
        self.FPSMeter.updatePosition()

class ImageViewerWindow(QMainWindow):

    def __init__(self, settingsWindow=None):
        super(ImageViewerWindow, self).__init__()
        self._settingsWindow = settingsWindow
        self.setupUi()
        quit = QAction("Quit", self)
        quit.triggered.connect(self.closeEvent)
        self.show()
    
    def setupUi(self):
        self._imView = QWidget()
        imViewLayout = QHBoxLayout(self._imView)
        self.imView = ImageViewer(self._imView)
        self.imView.setAlignment(Qt.AlignmentFlag.AlignCenter)
        imViewLayout.addWidget(self.imView)
        self.setCentralWidget(self._imView)
    
    def closeEvent(self, event):
        self._settingsWindow._unPinButton()