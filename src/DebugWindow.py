
from threading import Thread
from os.path import join as pjoin

from PyQt6 import QtCore
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtWidgets import QHBoxLayout, QVBoxLayout, QFrame

from components import resource_path
from components import CameraHandler
from components import SettingsManager
from components import DebugImageProcessor, createImageFromLayers
from components.UI import ImView, ImViewSecurityWidget, ImViewWindow
from components.UI import DrawerSettingsWidget
from components.UI import CameraSettingsWidget
from components.UI import ExportImportFrame
from components.UI import imViewControlPanel

ASSETS_FOLDER_PATH = resource_path("assets")

def runWindow():
    window = DebugWindow()
    window.show()

class DebugWindow(QFrame):

    def __init__(self, fps : int = 32, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.settingsManager = SettingsManager("cache")
        self.camera = CameraHandler()
        self.drawer = DebugImageProcessor(settingManager=self.settingsManager,camera=self.camera)
        self.imViews: list[ImView] = []
        self.createTimers(fps=fps)

        self.setObjectName("debugScreen")
        self.setupUI()
        self.setupStyles()
        self.imageTimer.start()

    def setupStyles(self):
        with open(pjoin(ASSETS_FOLDER_PATH, "styles/debugScreen.css")) as style:
            self.setStyleSheet(style.read())

    def setupUI(self):
        self.mainWidget = self
        self.mainLayout = QHBoxLayout(self)

        self.imViewsContainer = ImViewSecurityWidget(
            self.fps, self.imViews, objectName="mainImViewers")
        self.mainLayout.addWidget(self.imViewsContainer, stretch=3)

        self.settingsBar = SettingsBar(self, self.settingsManager, self.camera, self.drawer)
        self.mainLayout.addWidget(self.settingsBar)

    def createTimers(self, fps: int):
        self.fps = fps
        self.imageTimer = QTimer()
        self.imageTimer.timeout.connect(self.imViewsUpdate)
        self.imageTimer.setInterval(1000//self.fps)

    @property
    def reqLayers(self):
        layers = set()
        for imView in self.imViews:
            for layer in imView.layers:
                layers.add(layer)
        return list(layers)

    @QtCore.pyqtSlot()
    def imViewsUpdate(self):
        layers = self.drawer(self.reqLayers)
        for imView in self.imViews:
            if imView.isWorking:
                th = Thread(target=lambda layers, imView: imView.addImageToQueue(
                    createImageFromLayers(layers, imView.layers)), args=(layers, imView))
                th.start()


class SettingsBar(QFrame):

    def __init__(self, parent, settingManager : SettingsManager, camera: CameraHandler, drawer: DebugImageProcessor, *args, **kwargs):
        super().__init__(parent=parent, *args, **kwargs)
        self.mainWindow = parent
        self.camera = camera
        self.drawer = drawer

        self.settingsManager: SettingsManager = settingManager
        self.setupUI()

    def updateModules(self):
        raise NotImplementedError()
        # TODO this feature
        # self.cameraSettings.insert(newSettings)
        # self.drawerSettingsWid.updateSettings(newSettings)
        # self.cameraSettingsWid.updateSettings(newSettings)
        # self.imViewsControlPanel.updateSettings(newSettings)

    def setupUI(self):
        self.mainLayout = QVBoxLayout(self)
        self.mainLayout.setSpacing(25)

        self.separeteImView = ImViewWindow(fps=self.mainWindow.fps)
        self.mainWindow.imViews.append(self.separeteImView.imView)
        self.separeteImViewBtn = self.separeteImView.createSwitchBtn()

        self.drawerSettingsWid = DrawerSettingsWidget(drawer=self.drawer, settingsManager=self.settingsManager)

        self.cameraSettingsWid = CameraSettingsWidget(camera=self.camera, settingsManager=self.settingsManager)

        self.imViewsControlPanel = imViewControlPanel(
            self.mainWindow.imViewsContainer)

        self.settingsImExBtns = ExportImportFrame(
            self.settingsManager, self.updateModules)

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