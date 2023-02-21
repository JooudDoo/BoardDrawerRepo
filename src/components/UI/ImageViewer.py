import numpy as np

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QAction

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
        
    def setPixmap(self, pixmap):
        super(ImageViewer, self).setPixmap(pixmap.scaled(
            self.width()-25, self.height()-20,
            QtCore.Qt.KeepAspectRatio))

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