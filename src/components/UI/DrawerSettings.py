
from PyQt6.QtWidgets import QVBoxLayout, QHBoxLayout, QPushButton

from components.ImageProcessor import DebugImageProcessor
from components.UI.StyleModules import SettingsModule


class DrawerSettingsWidget(SettingsModule):

    def __init__(self, drawer: DebugImageProcessor, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.drawer = drawer

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

    def setupUI(self):
        self.mainLayout = QVBoxLayout(self)

        self.mainLayout.addLayout(self.createModeBtns())
