"""
    QLineEdit 美化文件
"""
# pylint: disable=no-name-in-module
from PySide6.QtGui import QAction, QContextMenuEvent
from PySide6.QtWidgets import QLineEdit
from . import Menu


class LineEdit(QLineEdit):
    """
    QLineEdit 美化
    """
    def __init__(self):
        super().__init__()
        self.right_menu_list = [
            ("Undo", self.undo, "Ctrl+Z"),
            ("Redo", self.redo, "Ctrl+Shift+Z"),
            ("Copy", self.copy, "Ctrl+C"),
            ("Paste", self.paste, "Ctrl+V"),
            ("Select All", self.selectAll, "Ctrl+A")
        ]

        self.menu = Menu("", self)
        for text, callback, shortcut in self.right_menu_list:
            action = QAction(text, self)
            action.triggered.connect(callback)
            action.setShortcut(shortcut)
            self.menu.addAction(action)

    def contextMenuEvent(self, event: QContextMenuEvent) -> None:
        self.menu.popup(event.globalPos())
