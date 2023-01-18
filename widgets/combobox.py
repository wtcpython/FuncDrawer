"""
    QCombobox 美化文件
"""
# pylint: disable=no-name-in-module
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QComboBox, QListWidget, QListWidgetItem, QItemDelegate)
from . import LineEdit


class ComboBox(QComboBox):
    """
    重写QComboBox
    """
    def __init__(self, items: list) -> None:
        super().__init__()
        self.setEditable(True)
        self.setItemDelegate(QItemDelegate(self))
        self.setLineEdit(LineEdit())
        self.line = LineEdit()
        self.setLineEdit(self.line)
        self.line.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.line.setReadOnly(True)
        self.list = QListWidget(self)
        self.list.setObjectName("ComboBoxView")
        for item in items:
            self.list_item = QListWidgetItem(item, self.list)
            self.list_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setModel(self.list.model())
        self.setView(self.list)
