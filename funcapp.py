"""
    函数绘图的主文件
    https://www.github.com/wtcpython/FuncDrawer/
"""
# pylint: disable=no-name-in-module
import sys
from effect import set_effect
from PySide6.QtGui import QIcon, QKeyEvent, Qt, QMouseEvent
from PySide6.QtWidgets import QApplication, QPushButton, QTabWidget, QWidget

from graph import Widget
from setting import Setting
from translate import tras, tmp_path


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

        self.setting_button = QPushButton(tras("Settings"))
        self.setting_button.clicked.connect(self.setting)
        self.setCornerWidget(self.setting_button)

        self.tab_button = QPushButton("＋", self)
        self.tab_button.clicked.connect(self.add_widget)
        self.tab_button.setFixedSize(32, 32)

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

    def setting(self):
        """
        打开设置界面
        """
        window = Setting()
        current_row = 0
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

    def keyPressEvent(self, event: QKeyEvent) -> None:
        """
        重写QT按键事件
        """
        ctrl = event.modifiers() == Qt.KeyboardModifier.ControlModifier
        key = event.key()
        if ctrl and key == Qt.Key.Key_Q:
            self.close()
        elif ctrl and key == Qt.Key.Key_T:
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
    app.setWindowIcon(QIcon(str(tmp_path/"icon.ico")))
    window = MainWidget()
    set_effect(app, window)
    window.showMaximized()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
