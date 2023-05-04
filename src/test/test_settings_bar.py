from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtWidgets import QApplication
import unittest
from unittest.mock import patch
import os
import sys

sys.path.insert(1, 'src/')
from DebugWindow import DebugWindow

from components.UI.DrawerSettings import DrawerSettingsWidget
from components.UI.CameraSettings import CameraSettingsWidget
from components.UI.ExportImportSettings import ExportImportFrame
from components.UI.ImageViewerControlPanel import imViewControlPanel


class TestSettingsBar(unittest.TestCase):

    # проверка настроек камеры на тип цветокора
    def test_camera_type(self):
        app = QApplication([])
        debug_window = DebugWindow()
        if debug_window.camera.status == 200:
            print(len(debug_window.settingsBar.mainLayout))
            self.assertTrue(debug_window.settingsBar.cameraSettings.rangeType == 'RGB' or 
                            debug_window.settingsBar.cameraSettings.rangeType == 'HSL')
        return True
    
    # проверяем количество стартовых экранов
    def test_len_window_start(self):
        app = QApplication([])
        debug_window = DebugWindow()
        if debug_window.camera.status == 200:
            self.assertEqual(len(debug_window.settingsBar.mainWindow.imViews), 5)
        return True

    # проверка, что все виджеты созданы и добавлены в основной макет 
    def test_init_class(self):
        app = QApplication([])
        debug_window = DebugWindow()
        if debug_window.camera.status == 200:
                assert isinstance(debug_window.settingsBar.drawerSettingsWid, DrawerSettingsWidget)
                assert isinstance(debug_window.settingsBar.cameraSettingsWid, CameraSettingsWidget)
                assert isinstance(debug_window.settingsBar.imViewsControlPanel, imViewControlPanel)
                assert isinstance(debug_window.settingsBar.settingsImExBtns, ExportImportFrame)
                assert debug_window.settingsBar.layout() is not None
        return True


if __name__ == '__main__':
    unittest.main()
