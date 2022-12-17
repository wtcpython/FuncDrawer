# coding:utf-8
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QMenu


class Menu(QMenu):
    def __init__(self, title: str, parent):
        super().__init__(title, parent)
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.Popup | Qt.WindowType.NoDropShadowWindowHint
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
