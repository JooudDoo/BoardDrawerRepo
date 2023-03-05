
from PyQt6.QtWidgets import QVBoxLayout, QHBoxLayout, QPushButton, QGridLayout
from PyQt6.QtCore import Qt

from components.ImageProcessor import DebugImageProcessor
from components.SettingsLoader import SettingsManager
from components.UI.RangeSlider import RangeSliderLabel, RangeSlider
from components.UI.StyleModules import SettingsModule


class DrawerSettingsWidget(SettingsModule):

    def __init__(self, settingsManager : SettingsManager, drawer: DebugImageProcessor, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.drawer = drawer
        self.settingsManager = settingsManager

        self.setupUI()

    def createModeBtns(self,):
        layout = QHBoxLayout()

        switchDrawModeBtn = QPushButton(
            text="Draw", objectName="debugSettingsBtn")
        cleanCanvasBtn = QPushButton(
            text="Clean canvas", objectName="debugSettingsBtn")

        def switchDrawModeBtnClicked():
            if self.drawer.switchDrawMode():
                switchDrawModeBtn.setText("No draw")
            else:
                switchDrawModeBtn.setText("Draw")

        switchDrawModeBtn.clicked.connect(switchDrawModeBtnClicked)
        cleanCanvasBtn.clicked.connect(self.drawer.cleanCanvas)

        layout.addWidget(switchDrawModeBtn)
        layout.addWidget(cleanCanvasBtn)
        return layout

    def createColorRangeSliders(self):
        if self.settingsManager.getSetting("ranges").rangeType == 'HSL':
            colors = ['hue', 'saturation', 'lightness']
        elif self.settingsManager.getSetting("ranges").rangeType == 'RGB':
            colors = ['red', 'green', 'blue']
        else:
            return
        layout = QGridLayout()

        minRangeLabel = RangeSliderLabel(
            "MinRange", self.settingsManager.getSetting("ranges"), 'minRange', objectName="settingTitle")
        layout.addWidget(minRangeLabel, 0, 0)
        layout.addWidget(RangeSlider().setup(0, 255,
                         self.settingsManager.getSetting("ranges").minRange, colors[0], minRangeLabel), 1, 0)
        layout.addWidget(RangeSlider().setup(0, 255,
                         self.settingsManager.getSetting("ranges").minRange, colors[1], minRangeLabel), 2, 0)
        layout.addWidget(RangeSlider().setup(0, 255,
                         self.settingsManager.getSetting("ranges").minRange, colors[2], minRangeLabel), 3, 0)

        maxRangeLabel = RangeSliderLabel(
            "MaxRange", self.settingsManager.getSetting("ranges"), 'maxRange', objectName="settingTitle")
        layout.addWidget(maxRangeLabel, 0, 1)
        layout.addWidget(RangeSlider().setup(0, 255,
                         self.settingsManager.getSetting("ranges").maxRange, colors[0], maxRangeLabel), 1, 1)
        layout.addWidget(RangeSlider().setup(0, 255,
                         self.settingsManager.getSetting("ranges").maxRange, colors[1], maxRangeLabel), 2, 1)
        layout.addWidget(RangeSlider().setup(0, 255,
                         self.settingsManager.getSetting("ranges").maxRange, colors[2], maxRangeLabel), 3, 1)

        return layout

    def setupUI(self):
        self.mainLayout = QVBoxLayout(self)

        rangeLayout = QHBoxLayout()
        rangeLayout.addLayout(self.createColorRangeSliders(), stretch=1)

        reduceSliderLayout = QVBoxLayout()

        reduceSliderLabel = RangeSliderLabel(
            "ReduceBy", self.settingsManager.getSetting("reduce"), field='val', objectName="settingTitle")
        reduceSlider = RangeSlider(Qt.Orientation.Vertical).setup(
            min=1, max=10, container=self.settingsManager.getSetting("reduce"), field='val', label=reduceSliderLabel)
        
        reduceSliderLayout.addWidget(reduceSliderLabel)
        reduceSliderLayout.addWidget(
            reduceSlider, alignment=Qt.AlignmentFlag.AlignHCenter)

        rangeLayout.addLayout(reduceSliderLayout, stretch=1)

        self.mainLayout.addLayout(self.createModeBtns())
        self.mainLayout.addLayout(rangeLayout)
