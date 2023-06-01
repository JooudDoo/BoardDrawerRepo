
import warnings

from PyQt6 import QtCore
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QPushButton, QHBoxLayout, QFileDialog

from components import VideoHandler
from components.SettingsLoader import SettingsManager
from components.UI.RangeSlider import RangeSliderLabel, RangeSlider
from components.UI.StyleModules import SettingsModule


class VideoSettingsWidget(SettingsModule):

    def __init__(self, settingsManager : SettingsManager, videoHandler: VideoHandler, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.videoHandler = videoHandler
        self.settingsManager = settingsManager
        self.setupUI()

    def setupUI(self):
        # TODO сделать возможность выбирать источник из камер для захвата
        layout = QHBoxLayout(self)

        selectCameraStream = QPushButton(
            text='WebCam', objectName="debugSettingsBtn")
        selectCameraStream.clicked.connect(self.cameraStream_btn)

        selectFileStream = QPushButton(
            text='File', objectName="debugSettingsBtn")
        selectFileStream.clicked.connect(self.fileStream_btn)

        layout.addWidget(selectCameraStream)
        layout.addWidget(selectFileStream)
        
    @QtCore.pyqtSlot()
    def cameraStream_btn(self):
        cameraID = 0
        change_status = self.videoHandler.change_source(new_src=cameraID)

        if not change_status:
            self.show_warning_pop(f"Not found camera id {cameraID}")


    @QtCore.pyqtSlot()
    def fileStream_btn(self):
        fname = QFileDialog.getOpenFileName(self, 'Select videofile to open')
        change_status = self.videoHandler.change_source(new_src=fname[0])

        if not change_status:
            self.show_warning_pop(f"Couldn't open {fname[0]}")

    @QtCore.pyqtSlot()
    def show_warning_pop(self, source_text):
        # TODO сделать всплывающие окно с ошибкой
        warnings.warn(f"Something wrong. Error text {source_text}")