
from PyQt6 import QtCore
from PyQt6.QtWidgets import QHBoxLayout, QPushButton, QFileDialog

from components.SettingsLoader import SettingsManager
from components.UI.StyleModules import SettingsModule


class ExportImportFrame(SettingsModule):

    def __init__(self, settingsManager: SettingsManager, updateGUIFunc, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUI()
        self.settingsManager = settingsManager
        self.updateGUI = updateGUIFunc

    def setupUI(self):
        layout = QHBoxLayout(self)

        saveSettingsBtn = QPushButton(
            text='Save', objectName="debugSettingsBtn")
        exportSettingsBtn = QPushButton(
            text='Export', objectName="debugSettingsBtn")
        importSettingsBtn = QPushButton(
            text='Import', objectName="debugSettingsBtn")

        def saveSettingsFunc(): return self.settingsManager.exportSettingsToJSON('cache')
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
            self.settingsManager.exportSettingsToJSON(fname[0])

    @QtCore.pyqtSlot()
    def importSettingsBtnF(self):
        fname = QFileDialog.getOpenFileName(self, 'Select file to import from')
        if fname[0]:
            self.settingsManager.importSettingsFromJSON(fname[0])
