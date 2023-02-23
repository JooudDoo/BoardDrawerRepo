
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton

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
        showMaskBtn = QPushButton(text="Show mask")

        def switchDrawModeBtnClicked():
            if self.drawer.switchDrawMode():
                switchDrawModeBtn.setText("No draw")
            else:
                switchDrawModeBtn.setText("Draw")

        def showMaskBtnClicked():
            if self.drawer.swictchMaskShowMode():
                showMaskBtn.setText("Hide mask")
            else:
                showMaskBtn.setText("Show mask")
        
        switchDrawModeBtn.clicked.connect(switchDrawModeBtnClicked)
        showMaskBtn.clicked.connect(showMaskBtnClicked)
        cleanCanvasBtn.clicked.connect(self.drawer.cleanCanvas)

        layout.addWidget(switchDrawModeBtn)
        layout.addWidget(showMaskBtn)
        layout.addWidget(cleanCanvasBtn)
        return layout

    def setupUI(self):
        self.mainLayout = QVBoxLayout(self)

        self.mainLayout.addLayout(self.createModeBtns())
