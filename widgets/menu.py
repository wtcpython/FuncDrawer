"""
    QMenu 美化文件
"""
# pylint: disable=no-name-in-module
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QMenu


class Menu(QMenu):
    """
    QMenu 美化
    """
    def __init__(self, title: str, parent):
        super().__init__(title, parent)
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.Popup | Qt.WindowType.NoDropShadowWindowHint
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
