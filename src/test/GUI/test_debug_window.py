from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtWidgets import QApplication
import unittest
from unittest.mock import patch
import os
import sys

sys.path.insert(1, 'src/')
from DebugWindow import DebugWindow


class TestDebugWindow(unittest.TestCase):

    # проверка на то что мы ожидаем в ответе при создании камеры 500 или 200
    def test_camera_error(self):
        app = QApplication([])
        debug_window = DebugWindow()
        self.assertTrue(debug_window.camera.status ==
                        500 or debug_window.camera.status == 200)

    # проверка загрузки стилистики
    def test_setupStyles(self):
        app = QApplication([])
        # Загрузите ожидаемые стили из файла CSS
        with open("src/styles/debugScreen.css", 'r') as expected_style_file:
            expected_style = expected_style_file.read()
        # Создайте экземпляр вашего класса виджета
        window = DebugWindow()
        # Запустите функцию setupStyles()
        window.setupStyles()
        # Сравните полученные стили с ожидаемыми
        self.assertEqual(window.styleSheet(), expected_style)

    # проверка на значение fsp
    def test_value_fps(self):
        app = QApplication([])
        window = DebugWindow(fps=24)
        self.assertEqual(window.fps, 24)

    # проверка чтения файла настроек
    def test_findFile(self):
        if os.path.isfile('cache'):
            self.assertTrue(True)
        else:
            self.assertTrue(False)

    # проверка на то есть ли тип в файле
    def test_type_in_file_for_settings(self):
        with open('cache', 'r', encoding='utf8') as importFile:
            type = importFile.readline().strip()
            self.assertTrue(type == 'RGB' or type == 'HSL')

    # проверка корректности имени окна
    def test_correct_name_window(self):
        app = QApplication([])
        window = DebugWindow()
        # Проверяем, что свойство objectName установлено правильно
        self.assertEqual(window.objectName(), "debugScreen")

    # проверка корректности запуска таймера
    @patch.object(QTimer, 'start')
    def test_correct_start_timer(self, mock_start):
        app = QApplication([])
        window = DebugWindow()
        window.imageTimer
        mock_start.assert_called_once()


if __name__ == '__main__':
    unittest.main()
