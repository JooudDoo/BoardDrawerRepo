
from PyQt5.QtWidgets import QSlider
from PyQt5.QtCore import Qt

class RangeSlider(QSlider):

    def __init__(self, orientation = Qt.Horizontal, parent = None):
        super(RangeSlider, self).__init__(orientation,parent)
    
    def setup(self, maxValue, updateValFunc, rgbContainer, colorName : str, connectedLabel):
        self.setMaximum(maxValue)
        self._updateValFunction = updateValFunc
        self._connectedValue = rgbContainer
        self._containerName = colorName
        self._connectedLabel = connectedLabel

        self._updatefunction = lambda x : self._connectedValue._updateColorByName(self._containerName, x)
        self.setValue(getattr(rgbContainer, colorName))
        self._connectedLabel.updateValue()
        self.valueChanged.connect(self.changeFunction)
        return self

    def changeFunction(self, val):
        self._updatefunction(val)
        self._updateValFunction()
        self._connectedLabel.updateValue()
    