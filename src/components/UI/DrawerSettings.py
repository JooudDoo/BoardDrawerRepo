
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton

from components.DrawerModule import Drawer

class DrawerSettingsWidget(QWidget):
    
    def __init__(self, drawer : Drawer, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.drawer = drawer

        self.setupUI()

    def createModeBtns(self,):
        layout = QHBoxLayout()

        switchDrawModeBtn = QPushButton(text="Draw")
        cleanCanvasBtn = QPushButton(text="Clean canvas")

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
