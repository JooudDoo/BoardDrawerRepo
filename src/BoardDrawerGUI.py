import sys

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import QMainWindow, QWidget, QApplication, QHBoxLayout, QVBoxLayout, QPushButton

from components.CameraHandler import CameraHandler, CameraSettings
from components.UI.ImageViewer import ImageViewer, ImageViewerWindow
from components.UI.RangeSlider import RangeSlider
from components.UI.RangeSliderLabel import RangeSliderLabel

def runGUI():
    app = QApplication([])
    window = CustomizerWindow()
    window.show()
    sys.exit(app.exec_())

class CustomizerWindow(QMainWindow):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.camera = CameraHandler()
        self.camera.loadSettings("cache")
        
        self._fps = 30
        self.mainTimer = QTimer()
        self.mainTimer.timeout.connect(self.imageUpdate)
        self.mainTimer.setInterval(1000//self._fps)
        self._imageViewerSize = (0, 0)

        self.setupUi()
        self.mainTimer.start()

    @QtCore.pyqtSlot()
    def imageUpdate(self):
        image = self.camera.getProcessedImage(self._imageViewerSize)
        image = QtGui.QImage(image.data, image.shape[1], image.shape[0], QtGui.QImage.Format_RGB888).rgbSwapped()
        self._currentImageViewer.setPixmap(QtGui.QPixmap.fromImage(image))
    
    def setupUi(self):
        self._mainWidget = QWidget(self)
        self._mainWidgetHorLayout = QHBoxLayout(self._mainWidget)
        
        self._imageViewer = ImageViewer()
        self._currentImageViewer = self._imageViewer
        self._mainWidgetHorLayout.addWidget(self._imageViewer, stretch=3)

        self._settingsBar = SettingsBar(self._mainWidget, self, self.camera)
        self._mainWidgetHorLayout.addWidget(self._settingsBar, stretch=1)

        self.setCentralWidget(self._mainWidget)

class SettingsBar(QWidget):
    
    def __init__(self, parent, mainWindow : CustomizerWindow, camera : CameraHandler):
        super().__init__(parent)
        self._mainWindow : CustomizerWindow = mainWindow
        self._camera = camera
        self.cameraSettings : CameraSettings = camera.settings
        self.setupUi()
    
    def updateCameraSettings(self):
        self._camera.setupSettings(self.cameraSettings)

    @QtCore.pyqtSlot()
    def _unPinButton(self):
        if self._isImageViewerPinned:
            self._imViewWin = ImageViewerWindow(self)
            self._mainWindow._currentImageViewer = self._imViewWin.imView
            self._isImageViewerPinned = False
        else:
            self._mainWindow._currentImageViewer = self._mainWindow._imageViewer
            self._imViewWin.close()
            self._isImageViewerPinned = True

    def _createRangeSliders(self, parent):
        grLayout = QtWidgets.QGridLayout(parent)
        print(self.cameraSettings)
        minRangeLabel = RangeSliderLabel("MinRange", self._camera.settings.minRange)
        if self._camera.settings.rangeType == 'HSL':
            colors = ['hue', 'saturation', 'lightness']
        elif self._camera.settings.rangeType == 'RGB': 
            colors = ['red', 'green', 'blue']
        grLayout.addWidget(minRangeLabel, 0, 0)
        grLayout.addWidget(RangeSlider().setup(255, self.updateCameraSettings, self._camera.settings.minRange, colors[0], minRangeLabel), 1, 0)
        grLayout.addWidget(RangeSlider().setup(255, self.updateCameraSettings, self._camera.settings.minRange, colors[1], minRangeLabel), 2, 0)
        grLayout.addWidget(RangeSlider().setup(255, self.updateCameraSettings, self._camera.settings.minRange, colors[2], minRangeLabel), 3, 0)

        maxRangeLabel = RangeSliderLabel("MaxRange", self._camera.settings.maxRange)
        grLayout.addWidget(maxRangeLabel, 0, 1)
        grLayout.addWidget(RangeSlider().setup(255, self.updateCameraSettings, self._camera.settings.maxRange, colors[0], maxRangeLabel), 1, 1)
        grLayout.addWidget(RangeSlider().setup(255, self.updateCameraSettings, self._camera.settings.maxRange, colors[1], maxRangeLabel), 2, 1)
        grLayout.addWidget(RangeSlider().setup(255, self.updateCameraSettings, self._camera.settings.maxRange, colors[2], maxRangeLabel), 3, 1)
    
    def _createImportExportBtns(self, parent):
        layout = QtWidgets.QHBoxLayout(parent)

        saveSettingsBtn = QtWidgets.QPushButton(text='Save')
        exportSettingsBtn = QtWidgets.QPushButton(text='Export')
        importSettingsBtn = QtWidgets.QPushButton(text='Import')

        saveSettingsFunc = lambda: CameraSettings.exportTo(self.cameraSettings, 'cache')
        saveSettingsBtn.clicked.connect(saveSettingsFunc)

        layout.addWidget(saveSettingsBtn)
        layout.addWidget(exportSettingsBtn)
        layout.addWidget(importSettingsBtn)

    def setupUi(self):
        self._mainLayout = QVBoxLayout(self)

        self._unPinImageFrameButton = QPushButton("Unpin image viewer")
        self._isImageViewerPinned = True
        self._unPinImageFrameButton.clicked.connect(self._unPinButton)

        self._rangeSlidersWid = QWidget()
        self._createRangeSliders(self._rangeSlidersWid)


        self._eximBtns = QWidget()
        self._createImportExportBtns(self._eximBtns)

        self._mainLayout.addWidget(self._unPinImageFrameButton, Qt.AlignmentFlag.AlignTop)
        self._mainLayout.addWidget(self._rangeSlidersWid, Qt.AlignmentFlag.AlignCenter)

        self._mainLayout.addWidget(self._eximBtns, Qt.AlignmentFlag.AlignBottom)