"""
    画板主文件
"""
# pylint: disable=no-name-in-module
# pylint: disable=unnecessary-lambda-assignment
import darkdetect
from pyqtgraph import PlotWidget, CONFIG_OPTIONS
from pyqtgraph.exporters import ImageExporter
from numpy import (
    absolute as Abs, arccos, arccosh, arcsin, arcsinh, arctan, pi, e,
    arctanh, cos, cosh, linspace, sin, sinh, sqrt, tan, tanh, log as ln,
    log10 as lg)
from PySide6.QtGui import QAction, QPen, QColor, Qt
from PySide6.QtWidgets import (QFileDialog, QMenuBar, QVBoxLayout, QPushButton,
                               QWidget, QHBoxLayout, QScrollArea)
from dialogs import FuncDialog
from setting import settings
from widgets import Menu
from translate import tras

# 这段没有任何意义，单纯不让flake8和pylint警告
_ = Abs(1) == arccos(1) == arccosh(1) == arcsin(1) == arcsinh(1) == \
    arctan(1) == arctanh(1) == cos(1) == cosh(1) == sin(1) == sinh(1) == \
    tan(1) == tanh(1) == lg(1)

log = lambda x, y: ln(y)/ln(x)
CONFIG_OPTIONS["antialias"] = settings["Anti-aliasing"] == "Enabled"


class Widget(QWidget):
    """
    主画板
    """
    def __init__(self):
        super().__init__()
        self.setWindowTitle(tras("New Figure"))

        self.scrollarea = QScrollArea(self)
        self.scrollarea.setWidgetResizable(True)
        self.widget = QWidget()
        self.lay = QVBoxLayout(self.widget)
        self.lay.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.scrollarea.setWidget(self.widget)

        self.mode = "black" if darkdetect.theme() == "Dark" and \
            settings["Window-Effect"] != "Default" else "white"
        self.plot = PlotWidget(background=self.mode)
        # self.plot.plotItem.addItem()
        self.plot.plotItem.resizeEvent = self.pass_event
        self.plot.plotItem.showGrid(True, True)
        self.plot.plotItem.setMenuEnabled(False)

        self.dialog = FuncDialog()
        self.dialog.signal.connect(self.draw_func)
        self.funclist = []

        self.menu_bar = QMenuBar(self)

        self.items1 = [(tras("Save as"), self.save_figure, "Ctrl+S")]
        self.items2 = [
            (tras("Draw"), self.dialog.show, "Alt+D"),
            (tras("Undo"), self.remove, "Ctrl+Z"),
            (tras("Clear"), self.plot.plotItem.clear, "Alt+C")
        ]

        self.add_menu(tras("File"), self.items1)
        self.add_menu(tras("Edit"), self.items2)

        self.hlayout2 = QHBoxLayout()
        self.hlayout2.addWidget(self.scrollarea, 1)
        self.hlayout2.addWidget(self.plot, 5)

        self.vlayout = QVBoxLayout(self)
        self.vlayout.addWidget(self.menu_bar, 1)
        self.vlayout.addLayout(self.hlayout2, 20)

    def add_menu(self, menu_text: str, item: list):
        """
        为菜单栏添加菜单
        """
        menu = Menu(menu_text, self)
        for text, callback, shortcut in item:
            action = QAction(text, self)
            action.triggered.connect(callback)
            action.setShortcut(shortcut)
            menu.addAction(action)
        self.menu_bar.addMenu(menu)

    def draw_func(self, dic: dict):
        """
        绘制函数图像的主函数
        """
        try:
            if (functype := dic["FuncType"]) == "f(x)=":
                x = linspace(-200, 200, 10**4+1)
                y = eval(dic["FuncName"])
                if isinstance(y, (int, float)):
                    x = (-10**9, 10**9)
                    y = (y, y)
            elif functype == "f(y)=":
                y = linspace(-200, 200, 10**4+1)
                x = eval(dic["FuncName"])
                if isinstance(x, (int, float)):
                    y = (-10**9, 10**9)
                    x = (x, x)
            elif functype == "normal":
                μ, σ = list(map(float, dic["FuncName"].split(",")))
                x = linspace(μ-300, μ+300, 10**6)
                y = (1/(sqrt(2*pi)*σ))*e**(-(x-μ)**2/(2*σ**2))

            pen = QPen(QColor("pink"), float(settings["line-thick"]))
            pen.setCosmetic(True)
            tmp = self.plot.plotItem.plot(x, y, pen=pen)
            self.funclist.append(tmp)
            # 添加解析式标签
            self.lay.addWidget(QPushButton(functype+dic["FuncName"]))
            self.dialog.close()
        except Exception:
            self.dialog.debug_line.setText(tras("Function input error!"))

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
