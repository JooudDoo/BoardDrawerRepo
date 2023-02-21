from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import Qt

class RangeSliderLabel(QLabel):

    def __init__(self, text, container, fieldName : str, parent=None):
        super(RangeSliderLabel, self).__init__(parent)
        self.cont = container
        self.fieldName = fieldName
        self._text = text
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setFixedHeight(25)
        self.setMinimumWidth(123)

    def updateValue(self):
        self.setText(f"{self._text}\n{str(getattr(self.cont, self.fieldName))}")