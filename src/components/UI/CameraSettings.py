
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QVBoxLayout, QGridLayout, QHBoxLayout, QWidget

from components.CameraHandler import CameraHandler
from components.SettingsLoader import SettingsManager
from components.UI.RangeSlider import RangeSliderLabel, RangeSlider
from components.UI.StyleModules import SettingsModule


class CameraSettingsWidget(SettingsModule):

    def __init__(self, settingsManager : SettingsManager, camera: CameraHandler, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.camera = camera
        self.settingsManager = settingsManager
        self.setupUI()

    def setupUI(self):
        return
