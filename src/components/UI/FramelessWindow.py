from PyQt6.QtCore import Qt, pyqtSignal, QPoint
from PyQt6.QtGui import QFont, QEnterEvent, QPainter, QColor, QPen
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QSpacerItem, QSizePolicy, QPushButton)


class FramelessWindow(QWidget):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)

        self.titleBar = TitleBar()
        self._mainlayout = QVBoxLayout(self)
        self._mainlayout.addWidget(self.titleBar)

        self.titleBar.windowMinimumed.connect(self.showMinimized)
        self.titleBar.windowMaximumed.connect(self.showMaximized)
        self.titleBar.windowNormaled.connect(self.showNormal)
        self.titleBar.windowClosed.connect(self.close)
        self.titleBar.windowMoved.connect(self.move)

    def move(self, pos):
        if self.windowState() == Qt.WindowState.WindowMaximized or self.windowState() == Qt.WindowState.WindowFullScreen:
            return
        super(FramelessWindow, self).move(pos)


class TitleBar(QWidget):

    # Сигнал минимизации окна
    windowMinimumed = pyqtSignal()
    # увеличить максимальный сигнал окна
    windowMaximumed = pyqtSignal()
    # сигнал восстановления окна
    windowNormaled = pyqtSignal()
    # сигнал закрытия окна
    windowClosed = pyqtSignal()
    # Окно мобильных
    windowMoved = pyqtSignal(QPoint)
    # Сигнал Своя Кнопка +++
    signalButtonMy = pyqtSignal()

    def __init__(self, *args, **kwargs):
        super(TitleBar, self).__init__(*args, **kwargs)

        # Поддержка настройки фона qss
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.mPos = None
        self.iconSize = 20                       # Размер значка по умолчанию

        # Установите цвет фона по умолчанию, иначе он будет прозрачным из-за влияния родительского окна
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(palette.ColorRole.Window, QColor(240, 240, 240))
        self.setPalette(palette)

        # макет
        layout = QHBoxLayout(self, spacing=0)
        layout.setContentsMargins(0, 0, 0, 0)

        # значок окна
        self.iconLabel = QLabel(self)
#         self.iconLabel.setScaledContents(True)
        layout.addWidget(self.iconLabel)

        # название окна
        self.titleLabel = QLabel(self)
        self.titleLabel.setMargin(2)
        layout.addWidget(self.titleLabel)

        # Средний телескопический бар
        layout.addSpacerItem(QSpacerItem(
            40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))

        # Использовать шрифты Webdings для отображения значков
        font = self.font() or QFont()
        font.setFamily('Webdings')

        # Своя Кнопка ++++++++++++++++++++++++++
        self.buttonMy = QPushButton(
            '@', self, clicked=self.showButtonMy, font=font, objectName='buttonMy')
        layout.addWidget(self.buttonMy)

        # Свернуть кнопку
        self.buttonMinimum = QPushButton(
            '0', self, clicked=self.windowMinimumed.emit, font=font, objectName='buttonMinimum')
        layout.addWidget(self.buttonMinimum)

        # Кнопка Max / restore
        self.buttonMaximum = QPushButton(
            '1', self, clicked=self.showMaximized, font=font, objectName='buttonMaximum')
        layout.addWidget(self.buttonMaximum)

        # Кнопка закрытия
        self.buttonClose = QPushButton(
            'r', self, clicked=self.windowClosed.emit, font=font, objectName='buttonClose')
        layout.addWidget(self.buttonClose)

        # начальная высота
        self.setHeight()

    # +++ Вызывается по нажатию кнопки buttonMy
    def showButtonMy(self):
        print("Своя Кнопка ")
        self.signalButtonMy.emit()

    def showMaximized(self):
        if self.buttonMaximum.text() == '1':
            # Максимизировать
            self.buttonMaximum.setText('2')
            self.windowMaximumed.emit()
        else:  # Восстановить
            self.buttonMaximum.setText('1')
            self.windowNormaled.emit()

    def setHeight(self, height=38):
        """ Установка высоты строки заголовка """
        self.setMinimumHeight(height)
        self.setMaximumHeight(height)
        # Задайте размер правой кнопки  ?
        self.buttonMinimum.setMinimumSize(height, height)
        self.buttonMinimum.setMaximumSize(height, height)
        self.buttonMaximum.setMinimumSize(height, height)
        self.buttonMaximum.setMaximumSize(height, height)
        self.buttonClose.setMinimumSize(height, height)
        self.buttonClose.setMaximumSize(height, height)

        self.buttonMy.setMinimumSize(height, height)
        self.buttonMy.setMaximumSize(height, height)

    def setTitle(self, title):
        """ Установить заголовок """
        self.titleLabel.setText(title)

    def setIcon(self, icon):
        """ настройки значокa """
        self.iconLabel.setPixmap(icon.pixmap(self.iconSize, self.iconSize))

    def setIconSize(self, size):
        """ Установить размер значка """
        self.iconSize = size

    def mousePressEvent(self, event):
        """ Событие клика мыши """
        if event.button() == Qt.MouseButton.LeftButton:
            self.mPos = event.pos()
        event.accept()

    def mouseReleaseEvent(self, event):
        ''' Событие отказов мыши '''
        self.mPos = None

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.MouseButton.LeftButton and self.mPos:
            self.windowMoved.emit(self.mapToGlobal(event.pos() - self.mPos))
        event.accept()
