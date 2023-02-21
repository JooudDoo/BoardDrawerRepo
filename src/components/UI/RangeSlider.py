
from PyQt5.QtWidgets import QSlider
from PyQt5.QtCore import Qt

class RangeSlider(QSlider):

    def __init__(self, orientation = Qt.Horizontal, parent = None):
        super(RangeSlider, self).__init__(orientation,parent)
    
    def setup(self, maxValue : int, updateValFunc, container, containerName : str, connectedLabel, minValue : int = 0):
        self.setMinimum(minValue)
        self.setMaximum(maxValue)
        self._updateValFunction = updateValFunc
        self._connectedValue = container
        self._containerName = containerName
        self._updatefunction = lambda x : self._connectedValue.__setattr__(self._containerName, x)
        self.setValue(getattr(self._connectedValue, self._containerName))
        self._connectedLabel = connectedLabel
        self._connectedLabel.updateValue()
        self.valueChanged.connect(self.changeFunction)
        return self

    def changeFunction(self, val):
        self._updatefunction(val)
        self._updateValFunction()
        self._connectedLabel.updateValue()
    