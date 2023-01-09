"""
    QLineEdit 美化文件
"""
# pylint: disable=no-name-in-module
from PySide6.QtGui import QAction, QContextMenuEvent
from PySide6.QtWidgets import QLineEdit
from . import Menu
# from ..translate import tras


class LineEdit(QLineEdit):
    """
    QLineEdit 美化
    """
    def __init__(self):
        super().__init__()
        self.right_menu_list = [
            ("Undo", self.undo),
            ("Redo", self.redo),
            ("Copy", self.copy),
            ("Paste", self.paste),
            ("Select All", self.selectAll)
        ]

        self.menu = Menu("", self)
        for text, callback in self.right_menu_list:
            action = QAction(text, self)
            action.triggered.connect(callback)
            self.menu.addAction(action)

    def contextMenuEvent(self, event: QContextMenuEvent) -> None:
        self.menu.popup(event.globalPos())
