
import re

from PyQt6 import QtCore
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QCheckBox, QGridLayout, QScrollArea, QFrame

from components.UI.ImageViewer import ImViewSecurityWidget, ImView
from components.DrawerModule import Filters
from components.UI.StyleModules import SettingsModule


class imViewControlPanel(SettingsModule):

    def __init__(self, imViewContainer, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.imViewCont = imViewContainer
        self.setupUI()

    def setupUI(self):
        layout = QGridLayout(self)

        for id, imView in enumerate(self.imViewCont):
            if imView.metadata:
                pos = re.search(r"POS<(\d+):(\d+)>", imView.metadata)
                if not pos:
                    continue
                row, column = [int(x) for x in pos.groups()]
                tuner = imViewTuner(self.imViewCont, id)
                layout.addWidget(tuner, row, column)


class imViewTuner(QWidget):

    def __init__(self, imViewsContainer: ImViewSecurityWidget, imViewID: int,  *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.imViewsContainer = imViewsContainer
        self.imViewID = imViewID
        self.imView = self.imViewsContainer[self.imViewID]
        self.imViewStateChanger = self.imViewsContainer.switchImView
        self.setupUi()

    @QtCore.pyqtSlot()
    def imViewCheckBoxChanged(self):
        self.imViewStateChanger(self.imViewID)

    def createImViewFiltersCheckBox(self, filters: list[Filters]):

        checkBoxWidget = QFrame(objectName="imViewFilters")
        layout = QVBoxLayout(checkBoxWidget)

        for filter in filters:
            checkBox = FilterCheckBox(filter, self.imView)
            layout.addWidget(checkBox)

        scrollArea = QScrollArea(objectName="imViewFilters")
        scrollArea.verticalScrollBar().setObjectName("imViewFilters")
        scrollArea.setWidget(checkBoxWidget)
        return scrollArea

    def setupUi(self):
        self.mainLayout = QVBoxLayout(self)

        self.imViewCheckBox = QCheckBox(objectName="tunerMainCheckBox")
        self.imViewCheckBox.setCheckState(
            Qt.CheckState.Checked if self.imView.isWorking else Qt.CheckState.Unchecked)
        self.imViewCheckBox.setText(f"Monitor {self.imViewID}")
        self.imViewCheckBox.stateChanged.connect(self.imViewCheckBoxChanged)

        self.filters = self.createImViewFiltersCheckBox([x for x in Filters])

        self.mainLayout.addWidget(self.imViewCheckBox)
        self.mainLayout.addWidget(self.filters)


class FilterCheckBox(QCheckBox):

    def __init__(self, filter: Filters, imView: ImView, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.filter = filter
        self.imView = imView
        self.setText(filter.value)
        self.stateChanged.connect(self.changeFunc)

    @QtCore.pyqtSlot()
    def changeFunc(self):
        if self.checkState() == Qt.CheckState.Checked:
            self.imView.addFilter(self.filter)
        else:
            self.imView.removeFilter(self.filter)
