"""
    画板主文件
"""
# pylint: disable=no-name-in-module
# pylint: disable=unnecessary-lambda-assignment
from pyqtgraph import PlotWidget
from pyqtgraph.exporters import ImageExporter
from numpy import (absolute, arccos, arccosh, arcsin, arcsinh, arctan, arctanh,
                   cos, cosh, e, linspace, pi, sin, sinh, sqrt, tan, tanh,
                   log as _log)
from PySide6.QtGui import QAction, Qt, QPen, QColor
from PySide6.QtCore import QSize
from PySide6.QtWidgets import (QFileDialog, QListWidget, QMenuBar,
                               QListWidgetItem, QVBoxLayout,
                               QWidget, QListView, QHBoxLayout)

from dialogs import FuncDialog
from setting import settings
from widgets import Menu
from translate import tras

# 这段没有任何意义，单纯不让flake8和pylint警告
_ = absolute(1) == arccos(1) == arccosh(1) == arcsin(1) == arcsinh(1) == \
    arctan(1) == arctanh(1) == cos(1) == cosh(1) == sin(1) == sinh(1) == \
    tan(1) == tanh(1)

ln = lambda x: _log(x)/_log(e)
lg = lambda x: _log(x)/_log(10)
log = lambda x, y: _log(y)/_log(x)


class ListWidget(QListWidget):
    """
    存储函数解析式的listwidget
    """
    def __init__(self, parent) -> None:
        super().__init__(parent)
        self.setMovement(QListView.Movement.Static)
        self.setSpacing(1)
        self.setCurrentRow(0)

    def add_widget(self, text: str):
        """
        添加解析式标签
        """
        item = QListWidgetItem(text, self)
        item.setFlags(Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled)
        item.setSizeHint(QSize(0, 25))
        item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)


class Widget(QWidget):
    """
    主画板
    """
    def __init__(self):
        super().__init__()
        self.setWindowTitle(tras("New Figure"))

        self.list_widget = ListWidget(self)

        self.plot = PlotWidget(background="white")
        self.plot.plotItem.resizeEvent = self.pass_event
        self.plot.plotItem.showGrid(True, True)
        self.plot.plotItem.setMenuEnabled(False)

        self.dialog = FuncDialog()
        self.dialog.signal.connect(self.draw_func)
        self.funclist = []

        self.menu_bar = QMenuBar(self)

        self.items1 = [(tras("Save as"), self.save_figure)]
        self.items2 = [
            (tras("map"), self.dialog.show),
            (tras("Undo"), self.remove),
            (tras("empty"), self.plot.plotItem.clear)
        ]

        self.add_menu(tras("File"), self.items1)
        self.add_menu(tras("Edit"), self.items2)

        self.hlayout2 = QHBoxLayout()
        self.hlayout2.addWidget(self.list_widget, 1)
        self.hlayout2.addWidget(self.plot, 5)

        self.vlayout = QVBoxLayout(self)
        self.vlayout.addWidget(self.menu_bar, 1)
        self.vlayout.addLayout(self.hlayout2, 20)

    def add_menu(self, menu_text: str, item: list):
        """
        为菜单栏添加菜单
        """
        menu = Menu(menu_text, self)
        for text, callback in item:
            action = QAction(text, self)
            action.triggered.connect(callback)
            menu.addAction(action)
        self.menu_bar.addMenu(menu)

    def draw_func(self, dic: dict):
        """
        绘制函数图像的主函数
        """
        try:
            if (functype := dic["FuncType"]) == "f(x)=":
                x = linspace(-30, 30, 50000)
                y = eval(dic["FuncName"])
                if isinstance(y, (int, float)):
                    x = (-1000, 1000)
                    y = (y, y)
            elif functype == "f(y)=":
                y = linspace(-30, 30, 50000)
                x = eval(dic["FuncName"])
                if isinstance(x, (int, float)):
                    y = (-1000, 1000)
                    x = (x, x)
            elif functype == "normal":
                μ, σ = list(map(float, dic["FuncName"].split(",")))
                x = linspace(μ-15, μ+15, 50000)
                y = (1/(sqrt(2*pi)*σ))*e**(-(x-μ)**2/(2*σ**2))
            # elif functype == "ellipse":
            #     lis = list(map(float, dic["FuncName"].split(",")))
            #     if len(lis) < 4:
            #         lis += [0]*(4-len(lis))
            #     a, b, x, y = lis
            #     tmp = Ellipse(xy=(x, y), width=2*a, height=2*b)
            # elif functype == "circle":
            #     lis = list(map(float, dic["FuncName"].split(",")))
            #     if len(lis) < 3:
            #         lis += [0]*(3-len(lis))
            #     r, x, y = lis
            #     tmp = Circle(xy=(x, y), radius=r)
            # if functype not in ("ellipse", "circle"):
            pen = QPen(QColor("pink"), 2)
            pen.setCosmetic(True)
            tmp = self.plot.plotItem.plot(x, y, pen=pen)
            # else:
            #     tmp.set_fill(False)
            #     self.ax.add_patch(tmp)
            self.funclist.append(tmp)
            self.add_label(dic["FuncName"])
            self.dialog.hide()
            self.dialog.debug_line.setText("")
        except Exception:
            self.dialog.debug_line.setText(tras("Function input error!"))

    def add_label(self, name: str):
        """
        添加解析式标签
        """
        self.list_widget.setCurrentRow(self.list_widget.count())
        self.list_widget.add_widget(name)

    def remove(self):
        """
        撤销上一个图像
        """
        if self.funclist:
            self.plot.plotItem.removeItem(self.funclist.pop())

    def save_figure(self):
        """
        保存图像
        """
        file_name = QFileDialog.getSaveFileName(
            self, tras("Save Image As"),
            settings["defaultPath"], """
            Portable NetWork Graphics(*.png);;
            Scalable Vector Graphics(*.svg);;
            Portable Document Format(*.pdf)
            """)[0]
        # dpi = int(settings["ImageDpi"])
        ex = ImageExporter(self.plot.plotItem)
        if file_name:
            ex.export(file_name)

    def pass_event(self, event):
        """
        pass
        """
        return event

    def resizeEvent(self, event) -> None:
        """
        重写QT事件
        """
        super().resizeEvent(event)
        width, height = self.plot.width() / 20, self.plot.height() / 20
        self.plot.setXRange(-width, width)
        self.plot.setYRange(-height, height)
