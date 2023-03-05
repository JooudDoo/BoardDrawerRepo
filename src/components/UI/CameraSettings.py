
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

    def updateCameraSettings(self):
        self.camera.setupSettings(self.cameraSettings)

    def createColorRangeSliders(self):
        if self.cameraSettings.rangeType == 'HSL':
            colors = ['hue', 'saturation', 'lightness']
        elif self.cameraSettings.rangeType == 'RGB':
            colors = ['red', 'green', 'blue']
        else:
            return
        layout = QGridLayout()

        minRangeLabel = RangeSliderLabel(
            "MinRange", self.cameraSettings, 'minRange', objectName="settingTitle")
        layout.addWidget(minRangeLabel, 0, 0)
        layout.addWidget(RangeSlider().setup(0, 255, self.updateCameraSettings,
                         self.cameraSettings.minRange, colors[0], minRangeLabel), 1, 0)
        layout.addWidget(RangeSlider().setup(0, 255, self.updateCameraSettings,
                         self.cameraSettings.minRange, colors[1], minRangeLabel), 2, 0)
        layout.addWidget(RangeSlider().setup(0, 255, self.updateCameraSettings,
                         self.cameraSettings.minRange, colors[2], minRangeLabel), 3, 0)

        maxRangeLabel = RangeSliderLabel(
            "MaxRange", self.cameraSettings, 'maxRange', objectName="settingTitle")
        layout.addWidget(maxRangeLabel, 0, 1)
        layout.addWidget(RangeSlider().setup(0, 255, self.updateCameraSettings,
                         self.cameraSettings.maxRange, colors[0], maxRangeLabel), 1, 1)
        layout.addWidget(RangeSlider().setup(0, 255, self.updateCameraSettings,
                         self.cameraSettings.maxRange, colors[1], maxRangeLabel), 2, 1)
        layout.addWidget(RangeSlider().setup(0, 255, self.updateCameraSettings,
                         self.cameraSettings.maxRange, colors[2], maxRangeLabel), 3, 1)

        return layout

    def setupUI(self):
        return
        self.mainLayout = QVBoxLayout(self)

        rangeLayout = QHBoxLayout()
        rangeLayout.addLayout(self.createColorRangeSliders(), stretch=1)

        reduceSliderLayout = QVBoxLayout()
        reduceSliderLabel = RangeSliderLabel(
            "ReduceBy", self.cameraSettings, field='maskReduceBy', objectName="settingTitle")
        reduceSlider = RangeSlider(Qt.Orientation.Vertical).setup(
            min=1, max=10, updateValFunc=self.updateCameraSettings, container=self.cameraSettings, field='maskReduceBy', label=reduceSliderLabel)
        reduceSliderLayout.addWidget(reduceSliderLabel)
        reduceSliderLayout.addWidget(
            reduceSlider, alignment=Qt.AlignmentFlag.AlignHCenter)

        rangeLayout.addLayout(reduceSliderLayout, stretch=1)

        self.mainLayout.addLayout(rangeLayout)
