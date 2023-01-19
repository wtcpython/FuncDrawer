"""
    设置主文件
"""
# pylint: disable=no-name-in-module
import json
import os
import sys

from PySide6.QtCore import Qt, qVersion
from PySide6.QtGui import QFontDatabase
from PySide6.QtWidgets import (
    QApplication, QHBoxLayout, QLabel, QListView, QListWidget,
    QListWidgetItem, QPushButton, QStackedWidget, QVBoxLayout, QWidget)

from translate import tras, settings, LANG
from widgets import ComboBox

__ver__ = "0.7.1"


class SettingWidgetBase(QWidget):
    """
    “设置”的基本类
    """
    def __init__(self, title: str):
        super().__init__()
        self.setWindowTitle(title)

        self.vlayout = QVBoxLayout(self)
        self.vlayout.setAlignment(Qt.AlignmentFlag.AlignTop)

    def add_layout(self, text: str, items: list) -> ComboBox:
        """
        添加一组对象，包括一个label和一个combobox
        """
        label = QLabel(text, self)
        box = ComboBox(items)
        layout = QHBoxLayout()
        layout.addWidget(label, 2)
        layout.addWidget(box, 3)
        self.vlayout.addLayout(layout)
        return box


class Setting(QWidget):
    """
    设置主界面
    """
    def __init__(self):
        super().__init__()
        self.setWindowTitle(tras("Settings"))

        self.stacked_widget = QStackedWidget()

        self.list_widget = QListWidget()
        self.list_widget.setMovement(QListView.Movement.Static)
        self.list_widget.setSpacing(3)
        self.list_widget.setCurrentRow(0)

        self.tip_label = QLabel(
            tras("Please restart after changing Settings"), self)
        self.restart_button = QPushButton(
            tras("Restart"), self)

        self.button_layout = QHBoxLayout()
        self.button_layout.addWidget(
            self.tip_label, 0, Qt.AlignmentFlag.AlignLeft)
        self.button_layout.addWidget(
            self.restart_button, 0, Qt.AlignmentFlag.AlignRight)

        self.h_layout = QHBoxLayout()
        self.h_layout.addWidget(self.list_widget, 1)
        self.h_layout.addWidget(self.stacked_widget, 3)

        self.v_layout = QVBoxLayout(self)
        self.v_layout.addLayout(self.h_layout)
        self.v_layout.addLayout(self.button_layout)

        self.stacked_widget.currentChanged.connect(self.current_widget_changed)
        self.list_widget.currentRowChanged.connect(
            self.stacked_widget.setCurrentIndex)
        self.restart_button.clicked.connect(self.apply_setting)

        self.add_widget(UIWidget())
        self.add_widget(FigureWidget())
        self.add_widget(AboutWidget())

    def apply_setting(self):
        """
        应用设置
        """
        for i in range(self.list_widget.count()-1):
            widget = self.stacked_widget.widget(i)
            widget.save_setting()
        with open("./settings.json", "w", encoding="UTF-8") as file:
            json.dump(settings, file, indent=4, ensure_ascii=False)
        QApplication.exit()
        os.startfile(sys.executable)

    def current_widget_changed(self, index: int):
        """
        当前设置页改变响应
        """
        if index == self.list_widget.count()-1:
            self.restart_button.setEnabled(False)
        else:
            self.restart_button.setEnabled(True)

    def add_widget(self, widget: QWidget):
        """
        添加一个设置页
        """
        self.list_widget.setCurrentRow(self.list_widget.count())
        self.stacked_widget.addWidget(widget)

        item = QListWidgetItem(widget.windowTitle(), self.list_widget)
        item.setFlags(Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled)
        item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)


class UIWidget(SettingWidgetBase):
    """
    UI设置页
    """
    def __init__(self):
        super().__init__("UI")

        self.font_box = self.add_layout(
            tras("Font"), QFontDatabase().families(
                QFontDatabase.WritingSystem.Any))
        self.font_box.setCurrentText(settings["Font"])

        self.font_size_box = self.add_layout(
            tras("Font Size"), map(str, range(16, 28, 2)))
        self.font_size_box.setCurrentText(settings["Font-Size"])

        self.language_box = self.add_layout(
            tras("Language"), ["Chinese", "English", "Japanese"])
        self.language_box.setCurrentText(LANG)

        self.effect_box = self.add_layout(
            tras("Window Effect"), ["Default", "Mica", "Acrylic", "Aero"])
        self.effect_box.setCurrentText(settings["Window-Effect"])

    def save_setting(self):
        """
        保存设置
        """
        settings["Font"] = self.font_box.currentText()
        settings["Font-Size"] = self.font_size_box.currentText()
        settings["language"] = self.language_box.currentText()
        settings["Window-Effect"] = self.effect_box.currentText()


class FigureWidget(SettingWidgetBase):
    """
    Figure设置页
    """
    def __init__(self):
        super().__init__("Figure")

        self.line_box = self.add_layout(tras("line thick"), map(str, range(6)))
        self.line_box.setCurrentText(settings["line-thick"])

        self.anti_box = self.add_layout(
            tras("Enable antialias image"), ["Enabled", "Disabled"])
        self.anti_box.setCurrentText(settings["Anti-aliasing"])

    def save_setting(self):
        """
        保存设置
        """
        settings["line-thick"] = self.line_box.currentText()
        settings["Anti-aliasing"] = self.anti_box.currentText()


class AboutWidget(QLabel):
    """
    关于页
    """
    def __init__(self,  parent=None) -> None:
        super().__init__(parent)
        self.setWindowTitle(tras("About"))
        self.setOpenExternalLinks(True)
        self.setText(f"""
        {tras("Func Drawer")} : {__ver__}
        Qt : {qVersion()}
        Designed by 王添成
        仓库 : https://github.com/wtcpython/FuncDrawer
        """)
