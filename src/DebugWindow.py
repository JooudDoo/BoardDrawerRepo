
from threading import Thread

from PyQt6 import QtCore
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtWidgets import QHBoxLayout, QVBoxLayout, QFrame

from components.CameraHandler import CameraHandler, CameraSettings
from components.DrawerModule import Drawer, createImageFromLayers
from components.UI.ImageViewer import ImView, ImViewSecurityWidget, ImViewWindow
from components.UI.DrawerSettings import DrawerSettingsWidget
from components.UI.CameraSettings import CameraSettingsWidget
from components.UI.ExportImportSettings import ExportImportFrame
from components.UI.ImageViewerControlPanel import imViewControlPanel


def runWindow():
    window = DebugWindow()
    window.show()


class DebugWindow(QFrame):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.camera = CameraHandler(settings='cache')
        self.drawer = Drawer(self.camera)
        self.imViews: list[ImView] = []
        self.createTimers()

        self.setObjectName("debugScreen")
        self.setupUI()
        self.setupStyles()
        self.imageTimer.start()

    def setupStyles(self):
        with open("src/styles/debugScreen.css", 'r') as style:
            self.setStyleSheet(style.read())

    def setupUI(self):
        self.mainWidget = self
        self.mainLayout = QHBoxLayout(self)

        self.imViewsContainer = ImViewSecurityWidget(
            self.fps, self.imViews, objectName="mainImViewers")
        self.mainLayout.addWidget(self.imViewsContainer, stretch=3)

        self.settingsBar = SettingsBar(self, self.camera, self.drawer)
        self.mainLayout.addWidget(self.settingsBar)

    def createTimers(self, fps: int = 35):
        self.fps = fps
        self.imageTimer = QTimer()
        self.imageTimer.timeout.connect(self.imViewsUpdate)
        self.imageTimer.setInterval(1000//self.fps)

    @QtCore.pyqtSlot()
    def imViewsUpdate(self):
        layers = self.drawer.drawer()
        for imView in self.imViews:
            if imView.isWorking:
                th = Thread(target=lambda layers, imView: imView.addImageToQueue(
                    createImageFromLayers(layers, imView.filters)), args=(layers, imView))
                th.start()


class SettingsBar(QFrame):

    def __init__(self, parent: DebugWindow, camera: CameraHandler, drawer: Drawer, *args, **kwargs):
        super().__init__(parent=parent, *args, **kwargs)
        self.mainWindow = parent
        self.camera = camera
        self.drawer = drawer

        self.cameraSettings: CameraSettings = camera.settings
        self.setupUI()

    def updateModules(self, newSettings: CameraSettings):
        # TODO this feature
        self.cameraSettings.insert(newSettings)
        self.drawerSettingsWid.updateSettings(newSettings)
        self.cameraSettingsWid.updateSettings(newSettings)
        self.imViewsControlPanel.updateSettings(newSettings)

    def setupUI(self):
        self.mainLayout = QVBoxLayout(self)
        self.mainLayout.setSpacing(25)

        self.separeteImView = ImViewWindow(fps=self.mainWindow.fps)
        self.mainWindow.imViews.append(self.separeteImView.imView)
        self.separeteImViewBtn = self.separeteImView.createSwitchBtn()

        self.drawerSettingsWid = DrawerSettingsWidget(self.drawer)

        self.cameraSettingsWid = CameraSettingsWidget(self.camera)

        self.imViewsControlPanel = imViewControlPanel(
            self.mainWindow.imViewsContainer)

        self.settingsImExBtns = ExportImportFrame(
            self.cameraSettings, self.updateModules)

        self.mainLayout.addWidget(
            self.separeteImViewBtn, Qt.AlignmentFlag.AlignCenter)
        self.mainLayout.addWidget(
            self.drawerSettingsWid, Qt.AlignmentFlag.AlignCenter)
        self.mainLayout.addWidget(
            self.cameraSettingsWid, Qt.AlignmentFlag.AlignCenter)
        self.mainLayout.addWidget(
            self.imViewsControlPanel, Qt.AlignmentFlag.AlignCenter)
        self.mainLayout.addWidget(
            self.settingsImExBtns, Qt.AlignmentFlag.AlignCenter)
