
from cv2 import Mat
import numpy as np
import time

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QAction, QLabel, QSizePolicy, QVBoxLayout, QPushButton

class FPSMeter(QLabel):
    def __init__(self,  *args, **kwargs):
        super(FPSMeter, self).__init__( *args, **kwargs)
        self.paddingLeft = 25
        self.paddingTop = 5
        self._fpsTimerPrev = time.time()
        self.imageUpdateCycleCount = 10
        self.imageUpdateCount = 0
        self.setText("")
    
    def FPSCalculation(self):
        self.imageUpdateCount += 1
        if self.imageUpdateCount >= self.imageUpdateCycleCount:
            sfromPrevUpdate = time.time() - self._fpsTimerPrev
            self._fpsTimerPrev = time.time()
            self.setText(f"FPS: {round(float(1/sfromPrevUpdate*self.imageUpdateCycleCount),2)}")
            self.imageUpdateCount = 0

    def updatePosition(self):
        if hasattr(self.parent(), 'viewport'):
            parentRect = self.parent().viewport().rect()
        else:
            parentRect = self.parent().rect()
        if not parentRect: return

        x = parentRect.width() - self.width() - self.paddingLeft
        y = self.paddingTop
        self.setGeometry(x, y, self.width(), self.height())
    
    def resizeEvent(self, a0: QtGui.QResizeEvent) -> None:
        super().resizeEvent(a0)
        self.updatePosition()

class ImView(QWidget):

    def __init__(self, name : str = "", metadata : str = None,  *args, **kwargs):
        super(ImView, self).__init__(*args, **kwargs)
        self.mainLayout = QVBoxLayout(self)

        self.imageLabel = QLabel()
        sizePolicy = QSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self.imageLabel.setMinimumSize(360, 360)
        self.imageLabel.setSizePolicy(sizePolicy)
        self.imageLabel.setScaledContents(False)

        self.mainLayout.addWidget(self.imageLabel)

        self.FPSMeter = FPSMeter(parent=self)
        self.loadDefaultImage()
        self.metadata = metadata
        self.isWorking = True

    def loadDefaultImage(self):
        try:
            self.setPixmap(QtGui.QPixmap("assets/defaultImage.jpg"))
        except:
            self.setImage(np.zeros((360, 360, 3)))

    def setImage(self, image : Mat):
        image = QtGui.QImage(image.data, image.shape[1], image.shape[0], QtGui.QImage.Format_RGB888).rgbSwapped()
        self.setPixmap(QtGui.QPixmap.fromImage(image))

    def setPixmap(self, pixmap):
        self.FPSMeter.FPSCalculation()
        self.imageLabel.setPixmap(pixmap.scaled(
            self.imageLabel.width(), self.imageLabel.height(),
            QtCore.Qt.KeepAspectRatio))
    
    def resizeEvent(self, a0: QtGui.QResizeEvent) -> None:
        super().resizeEvent(a0)
        self.FPSMeter.updatePosition()
    
    def setState(self, newState : bool):
        #Sets on/off if necessary returns new state
        if newState == self.isWorking:
            return self.isWorking
        return self.switchState()

    def switchState(self):
        #switch state to opposite returns new state
        self.isWorking = not self.isWorking
        if self.isWorking:
            self.show()
        else:
            self.hide()
        return self.isWorking

class ImViewWindow(QMainWindow):

    def __init__(self):
        super(ImViewWindow, self).__init__()
        self.setupUi()
        self.isShow = False
        self.switchBtn = None
        quit = QAction("Quit", self)
        quit.triggered.connect(self.closeEvent)
    
    @QtCore.pyqtSlot()
    def switchBtnFunc(self):
        self.isShow = not self.isShow
        if self.isShow:
            self.switchBtn.setText("Hide window")
            self.imView.isWorking = True
            self.show()
        else:
            self.switchBtn.setText("Show window")
            self.imView.isWorking = False
            self.hide()

    def createSwitchBtn(self):
        if self.switchBtn:
            return self.switchBtn
        self.switchBtn = QPushButton()
        self.switchBtn.setText("Show window")
        self.switchBtn.clicked.connect(self.switchBtnFunc)

        return self.switchBtn

    def setupUi(self):
        self._imView = QWidget()
        imViewLayout = QHBoxLayout(self._imView)
        self.imView = ImView(self._imView)
        imViewLayout.addWidget(self.imView)
        self.setCentralWidget(self._imView)
    
    def closeEvent(self, event):
        self.switchBtnFunc()

class ImViewSecurityWidget(QWidget):

    def __init__(self, imViewsContainer : list[ImView], parent = None, rows = 2, columns = 2):
        super(ImViewSecurityWidget, self).__init__(parent)
        self.imViewContainer = imViewsContainer
        self.rows = rows
        self.columns = columns
        self.setupUi()

    def setupUi(self):
        self.mainLayout = QtWidgets.QGridLayout(self)

        for row in range(self.rows):
            for column in range(self.columns):
                imView = ImView(metadata=f"POS<{row}:{column}>")
                self.imViewContainer.append(imView)
                self.mainLayout.addWidget(imView, row, column)

    def __getitem__(self, ind) -> ImView:
        return self.imViewContainer[ind]

    def switchImView(self, ind, newState : bool = None):
        imView = self[ind]
        if newState == None:
            returnState = imView.switchState()
        else:
            returnState = imView.setState(newState)
        return returnState