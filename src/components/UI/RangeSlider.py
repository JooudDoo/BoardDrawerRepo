
from PyQt6.QtWidgets import QSlider, QLabel
from PyQt6.QtCore import Qt

class RangeSlider(QSlider):

    def __init__(self, orientation = Qt.Orientation.Horizontal, parent = None):
        super().__init__(orientation,parent)
    
    def setup(self, min : int = 0, max : int = 0, updateValFunc = None, container = None, field : str = "", label : QLabel = None):
        self.setMinimum(min)
        self.setMaximum(max)
        self._updateValFunction = updateValFunc
        self._connectedValue = container
        self._containerName = field
        self._updatefunction = lambda x : setattr(self._connectedValue, self._containerName, x)
        self.setValue(getattr(self._connectedValue, self._containerName))
        self._connectedLabel = label
        self._connectedLabel.updateValue()
        self.valueChanged.connect(self.changeFunction)
        return self

    def changeFunction(self, val):
        self._updatefunction(val)
        self._updateValFunction()
        self._connectedLabel.updateValue()
    
class RangeSliderLabel(QLabel):

    def __init__(self, text, container, field : str, parent=None):
        super().__init__(parent)
        self.cont = container
        self.fieldName = field
        self._text = text
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setFixedHeight(25)
        self.setMinimumWidth(123)

    def updateValue(self):
        self.setText(f"{self._text}\n{str(getattr(self.cont, self.fieldName))}")