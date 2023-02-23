
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QGridLayout, QHBoxLayout

from components.CameraHandler import CameraHandler
from components.UI.RangeSlider import RangeSliderLabel, RangeSlider

class CameraSettingsWidget(QWidget):
    
    def __init__(self, camera : CameraHandler, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.camera = camera
        self.cameraSettings = self.camera.settings

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

        minRangeLabel = RangeSliderLabel("MinRange", self.cameraSettings, field='minRange')
        layout.addWidget(minRangeLabel, 0, 0)
        layout.addWidget(RangeSlider().setup(max=255, updateValFunc=self.updateCameraSettings, container=self.cameraSettings.minRange, field=colors[0], label=minRangeLabel), 1, 0)
        layout.addWidget(RangeSlider().setup(max=255, updateValFunc=self.updateCameraSettings, container=self.cameraSettings.minRange, field=colors[1], label=minRangeLabel), 2, 0)
        layout.addWidget(RangeSlider().setup(max=255, updateValFunc=self.updateCameraSettings, container=self.cameraSettings.minRange, field=colors[2], label=minRangeLabel), 3, 0)

        maxRangeLabel = RangeSliderLabel("MaxRange", self.cameraSettings, field='maxRange')
        layout.addWidget(maxRangeLabel, 0, 1)
        layout.addWidget(RangeSlider().setup(max=255, updateValFunc=self.updateCameraSettings, container=self.cameraSettings.maxRange, field=colors[0], label=maxRangeLabel), 1, 1)
        layout.addWidget(RangeSlider().setup(max=255, updateValFunc=self.updateCameraSettings, container=self.cameraSettings.maxRange, field=colors[1], label=maxRangeLabel), 2, 1)
        layout.addWidget(RangeSlider().setup(max=255, updateValFunc=self.updateCameraSettings, container=self.cameraSettings.maxRange, field=colors[2], label=maxRangeLabel), 3, 1)
        return layout

    def setupUI(self):
        self.mainLayout = QVBoxLayout(self)

        rangeLayout = QHBoxLayout()
        rangeLayout.addLayout(self.createColorRangeSliders(), stretch=1)

        reduceSliderLayout = QVBoxLayout()
        reduceSliderLabel = RangeSliderLabel("ReduceBy", self.cameraSettings, field='maskReduceBy')
        reduceSlider = RangeSlider(Qt.Vertical).setup(min=1, max=10, updateValFunc=self.updateCameraSettings, container=self.cameraSettings, field='maskReduceBy', label=reduceSliderLabel)
        reduceSliderLayout.addWidget(reduceSliderLabel)
        reduceSliderLayout.addWidget(reduceSlider, alignment=Qt.AlignmentFlag.AlignHCenter)

        rangeLayout.addLayout(reduceSliderLayout, stretch=1)
        
        self.mainLayout.addLayout(rangeLayout)