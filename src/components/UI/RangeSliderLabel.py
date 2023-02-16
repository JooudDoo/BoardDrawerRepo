from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import Qt
from CameraHandler import RGB

class RangeSliderLabel(QLabel):

    def __init__(self, text, rgbContaier : RGB, parent=None):
        super(RangeSliderLabel, self).__init__(parent)
        self.rgb = rgbContaier
        self._text = text
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setFixedHeight(25)
        self.setText(rgbContaier.maximizedString())
        self.setMinimumWidth(123)

    def updateValue(self):
        self.setText(f"{self._text}\n{str(self.rgb)}")