
from PyQt6 import QtCore
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QPushButton

from components.CameraHandler import CameraHandler, CameraSettings
from components.DrawerModule import Drawer
from components.UI.ImageViewer import ImView, ImViewSecurityWidget, ImViewWindow
from components.UI.DrawerSettings import DrawerSettingsWidget
from components.UI.CameraSettings import CameraSettingsWidget

def runWindow():
    window = DebugWindow()
    window.show()

class DebugWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.camera = CameraHandler(settings='cache')
        self.drawer = Drawer(self.camera)
        self.imViews : list[ImView] = []
        self.createTimers()

        self.setupUI()

        self.imageTimer.start()

    def setupUI(self):
        self.mainWidget = QWidget()
        self.mainLayout = QHBoxLayout(self.mainWidget)
        self.setCentralWidget(self.mainWidget)

        self.imViewsContainer = ImViewSecurityWidget(self.imViews)
        self.mainLayout.addWidget(self.imViewsContainer, stretch=3)

        self.settingsBar = SettingsBar(self, self.camera, self.drawer)
        self.mainLayout.addWidget(self.settingsBar)

    def createTimers(self, fps : int = 30):
        self.fps = fps
        self.imageTimer = QTimer()
        self.imageTimer.timeout.connect(self.imViewsUpdate)
        self.imageTimer.setInterval(1000//self.fps)

    @QtCore.pyqtSlot()
    def imViewsUpdate(self):
        image = self.drawer.drawer()
        for imView in self.imViews:
            if imView.isWorking:
                imView.setImage(image)


class SettingsBar(QWidget):

    def __init__(self, parent : DebugWindow, camera : CameraHandler, drawer : Drawer, *args, **kwargs):
        super().__init__(parent=parent,*args, **kwargs)
        self.mainWindow = parent
        self.camera = camera
        self.drawer = drawer

        self.cameraSettings : CameraSettings = camera.settings
        self.setupUI()
    
    def createImportExportBtns(self):
        wid = QWidget()
        layout = QHBoxLayout(wid)

        saveSettingsBtn = QPushButton(text='Save')
        exportSettingsBtn = QPushButton(text='Export')
        importSettingsBtn = QPushButton(text='Import')

        saveSettingsFunc = lambda: CameraSettings.exportTo(self.cameraSettings, 'cache')
        saveSettingsBtn.clicked.connect(saveSettingsFunc)

        layout.addWidget(saveSettingsBtn)
        layout.addWidget(exportSettingsBtn)
        layout.addWidget(importSettingsBtn)

        return wid

    def setupUI(self):
        self.mainLayout = QVBoxLayout(self)

        self.separeteImView = ImViewWindow()
        self.mainWindow.imViews.append(self.separeteImView.imView)
        self.separeteImViewBtn = self.separeteImView.createSwitchBtn()
    
        self.drawerSettingsWid = DrawerSettingsWidget(self.drawer)

        self.cameraSettingsWid = CameraSettingsWidget(self.camera)

        self.imViewsControlPanel = None

        self.settingsImExBtns = self.createImportExportBtns()

        self.mainLayout.addWidget(self.separeteImViewBtn, Qt.AlignmentFlag.AlignCenter)
        self.mainLayout.addWidget(self.drawerSettingsWid, Qt.AlignmentFlag.AlignCenter)
        self.mainLayout.addWidget(self.cameraSettingsWid, Qt.AlignmentFlag.AlignCenter)
        self.mainLayout.addWidget(self.imViewsControlPanel, Qt.AlignmentFlag.AlignCenter)
        self.mainLayout.addWidget(self.settingsImExBtns, Qt.AlignmentFlag.AlignCenter)