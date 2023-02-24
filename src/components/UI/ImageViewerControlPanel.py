
from PyQt6 import QtWidgets, QtCore
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QCheckBox

from components.UI.ImageViewer import ImViewSecurityWidget

class imViewControlPanel(QWidget):
    pass

class imViewTuner(QWidget):

    def __init__(self, imViewsContainer : ImViewSecurityWidget, imViewID : int,  *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.imViewsContainer = imViewsContainer
        self.imViewID = imViewID
        self.imView = self.imViewsContainer[self.imViewID]
        self.imViewStateChanger = self.imViewsContainer.switchImView
        self.setupUi()
    
    @QtCore.pyqtSlot()
    def imViewCheckBoxChanged(self):
        self.imViewStateChanger(self.imViewID)

    def setupUi(self):
        self.mainLayout = QVBoxLayout(self)

        self.imViewCheckBox = QCheckBox()
        self.imViewCheckBox.setCheckState(self.imView.isWorking * 2) # magic to transfrom from True/False to 2/0
        self.imViewCheckBox.setText(f"Monitor {self.imViewID}")
        self.imViewCheckBox.stateChanged.connect(self.imViewCheckBoxChanged)

        self.mainLayout.addWidget(self.imViewCheckBox)