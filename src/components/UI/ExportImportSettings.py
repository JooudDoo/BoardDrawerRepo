
from PyQt6 import QtCore
from PyQt6.QtWidgets import QHBoxLayout, QPushButton, QFileDialog

from components.CameraHandler import CameraSettings
from components.UI.StyleModules import SettingsModule


class ExportImportFrame(SettingsModule):

    def __init__(self, cameraSettings: CameraSettings, settingsUpdater, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUI()
        self.cameraSettings = cameraSettings
        self.updateSettings = settingsUpdater

    def setupUI(self):
        layout = QHBoxLayout(self)

        saveSettingsBtn = QPushButton(
            text='Save', objectName="debugSettingsBtn")
        exportSettingsBtn = QPushButton(
            text='Export', objectName="debugSettingsBtn")
        importSettingsBtn = QPushButton(
            text='Import', objectName="debugSettingsBtn")

        def saveSettingsFunc(): return CameraSettings.exportTo(self.cameraSettings, 'cache')
        saveSettingsBtn.clicked.connect(saveSettingsFunc)
        exportSettingsBtn.clicked.connect(self.exporSettingsBtnF)
        importSettingsBtn.clicked.connect(self.importSettingsBtnF)

        layout.addWidget(saveSettingsBtn)
        layout.addWidget(exportSettingsBtn)
        layout.addWidget(importSettingsBtn)

    @QtCore.pyqtSlot()
    def exporSettingsBtnF(self):
        fname = QFileDialog.getOpenFileName(self, 'Select file to export to')
        if fname[0]:
            CameraSettings.exportTo(self.cameraSettings, fname[0])

    @QtCore.pyqtSlot()
    def importSettingsBtnF(self):
        fname = QFileDialog.getOpenFileName(self, 'Select file to import from')
        if fname[0]:
            self.cameraSettings = CameraSettings.importFrom(fname[0])
            self.updateSettings(self.cameraSettings)
