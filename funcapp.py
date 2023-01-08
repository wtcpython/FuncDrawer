"""
    函数绘图的主文件
    https://www.github.com/wtcpython/FuncDrawer/
"""
# pylint: disable=no-name-in-module
import sys
import webbrowser
import win32mica

from PySide6.QtGui import QAction, QIcon, QKeyEvent, Qt, QMouseEvent
from PySide6.QtWidgets import (QApplication, QPushButton, QTabWidget,
                               QTextEdit, QWidget)

from widgets import Menu
from graph import Widget
from setting import Setting
from translate import tras, settings


class MainWidget(QTabWidget):
    """
    带有标签页的主窗口
    """
    def __init__(self):
        super().__init__()
        self.setWindowTitle(tras("Func Drawer"))

        self.setTabsClosable(True)
        self.tabCloseRequested.connect(self.remove_tab)
        self.setMovable(True)
        self.setUsesScrollButtons(True)

        self.icon_button = QPushButton(QIcon("icon.ico"), "")
        self.setCornerWidget(self.icon_button, Qt.Corner.TopLeftCorner)

        self.tab_button = QPushButton("+", self)
        self.tab_button.clicked.connect(self.add_widget)
        self.tab_button.setFixedSize(32, 32)

        self.update_md = QTextEdit()
        self.update_md.setReadOnly(True)
        with open("./update.md", encoding="UTF-8") as file:
            self.update_md.setMarkdown(file.read())

        self.menu_list = [
            (tras("Settings"), self.setting),
            (tras("About"), self.about),
            (tras("update log"), self.open_update),
            (tras("Github Project"), self.open_gh)]

        self.menu = Menu("", self)
        for text, callback in self.menu_list:
            action = QAction(text, self)
            action.triggered.connect(callback)
            self.menu.addAction(action)
        self.icon_button.setMenu(self.menu)

        self.addTab(QWidget(), "")
        self.tabbar = self.tabBar()
        self.tabbar.setTabButton(
            self.count()-1,
            self.tabbar.ButtonPosition.LeftSide, self.tab_button)
        self.tabbar.setTabButton(
            self.count()-1,
            self.tabbar.ButtonPosition.RightSide, None)
        self.tabbar.setTabEnabled(self.count()-1, False)
        self.add_widget()

    def add_widget(self):
        """
        新增一个标签页，并定位到新标签页的位置
        """
        widget = Widget()
        self.insertTab(self.count()-1, widget, widget.windowTitle())
        self.setCurrentIndex(self.count()-2)

    def remove_tab(self, index: int):
        """
        移除标签页
        """
        self.removeTab(index)
        self.setCurrentIndex(self.count()-2)
        if self.count() <= 1:
            self.close()

    def setting(self, about=False):
        """
        打开设置界面
        """
        window = Setting()
        current_row = window.list_widget.count()-1 if about else 0
        window.list_widget.setCurrentRow(current_row)
        for i in range(self.count()):
            if self.widget(i).windowTitle() == tras("Settings"):
                self.setCurrentIndex(i)
                current_widget = self.currentWidget()
                current_widget.list_widget.setCurrentRow(current_row)
                break
        else:
            self.insertTab(self.count()-1, window, window.windowTitle())
            self.setCurrentIndex(self.count()-2)

    def about(self):
        """
        打开关于界面
        """
        self.setting(True)

    def open_update(self):
        """
        打开更新日志
        """
        self.insertTab(self.count()-1, self.update_md, tras("update log"))
        self.setCurrentIndex(self.count()-2)

    def open_gh(self):
        """
        打开本软件GitHub网站
        """
        webbrowser.open("https://www.github.com/wtcpython/FuncDrawer")

    def keyPressEvent(self, event: QKeyEvent) -> None:
        """
        重写QT按键事件
        """
        ctrl = event.modifiers() == Qt.KeyboardModifier.ControlModifier
        key = event.key()
        if ctrl and key == Qt.Key.Key_Q:
            self.close()
        elif ctrl and key == Qt.Key.Key_N:
            self.add_widget()
        elif ctrl and key == Qt.Key.Key_Tab:
            index = self.currentIndex()
            if index:
                self.setCurrentIndex(index-1)
            else:
                self.setCurrentIndex(self.count()-1)

    def mousePressEvent(self, event: QMouseEvent) -> None:
        """
        重写QT鼠标点击事件
        """
        super().mousePressEvent(event)
        if event.button() == Qt.MouseButton.MiddleButton:
            index = self.tabbar.tabAt(event.position().toPoint())
            if index >= 0:
                self.remove_tab(index)


def main():
    """
    主函数
    """
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("icon.ico"))
    app.setStyle("Fusion")
    app.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    with open("./style.qss", encoding="UTF-8") as file:
        style = file.read()
    style += f"*{'{'}font:{settings['Font-Size']}px '{settings['Font']}'{'}'}"
    app.setStyleSheet(style)
    window = MainWidget()
    window.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
    hwnd = window.winId()
    win32mica.ApplyMica(hwnd, win32mica.MICAMODE.DARK)
    window.showMaximized()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
