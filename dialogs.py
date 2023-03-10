"""
    对话框主文件
"""
# pylint: disable=no-name-in-module
from PySide6.QtCore import Signal
from PySide6.QtGui import Qt, QKeyEvent
from PySide6.QtWidgets import QPushButton, QGridLayout, QDialog
from effect import set_effect
from translate import tras
from widgets import LineEdit, ComboBox


names = ["", "", "", "", "Back",
         "round(", "(", ")", "Abs(", "sqrt(",
         "7", "8", "9", "**", "%",
         "4", "5", "6", "*", "/",
         "1", "2", "3", "+", "-",
         "0", ".", ",", "x", ""]
box1 = [tras("Trig func"), "sin(", "cos(", "tan(", "sinh(", "cosh(", "tanh("]
box2 = [tras("Inverse trig"), "arcsin(", "arccos(", "arctan(",
        "arcsinh(", "arccosh(", "arctanh("]
box3 = [tras("Log func"), "log(", "lg(", "ln(", "sqrt(", "abs("]
box4 = [tras("constant"), "e", "pi"]
ctl_key = [Qt.Key.Key_Delete, Qt.Key.Key_Left, Qt.Key.Key_Right,
           Qt.Key.Key_Enter, Qt.Key.Key_Backspace, Qt.Key.Key_Return]


class FuncLineEdit(LineEdit):
    """
    键入函数的输入框
    """
    def __init__(self):
        super().__init__()
        self.his_list = []
        self.his_pos = 0
        self.setPlaceholderText(
            tras("Use KeyBoard or click the Button to edit"))
        self.setAttribute(Qt.WidgetAttribute.WA_InputMethodEnabled, False)

    def back(self):
        """
        窗口界面上的退格键响应的事件
        """
        text = self.text()
        pos = self.cursorPosition()
        if text[:pos]:
            self.setText(text[:pos-1]+text[pos:])
            self.setCursorPosition(pos-1)

    def keyPressEvent(self, event: QKeyEvent) -> None:
        """
        重写QT按键事件
        """
        text = event.text()
        key = event.key()
        if text not in "wfjk;''[]zvm_WYFJK{}" or \
                key in ctl_key:
            super().keyPressEvent(event)


class FuncDialog(QDialog):
    """
    绘制函数的对话框
    """

    signal = Signal(dict)

    def __init__(self):
        super().__init__()
        self.setWindowTitle(tras("Func Drawer"))
        self.signal.emit({})
        set_effect(None, self)

        self.glayout = QGridLayout(self)
        self.glayout.setSpacing(10)
        self.glayout.setContentsMargins(10, 35, 10, 5)

        self.func_type = ComboBox(["f(x)=", "f(y)=", "normal", "ellipse",
                                  "circle"])
        self.func_type.currentTextChanged.connect(self.change_xy)
        self.glayout.addWidget(self.func_type, 0, 0)

        self.display = FuncLineEdit()
        self.glayout.addWidget(self.display, 0, 1, 1, 4)

        self.func_box1 = ComboBox(box1)
        self.func_box1.currentTextChanged.connect(self.box_cicked)

        self.func_box2 = ComboBox(box2)
        self.func_box2.currentTextChanged.connect(self.box_cicked)

        self.func_box3 = ComboBox(box3)
        self.func_box3.currentTextChanged.connect(self.box_cicked)

        self.func_box4 = ComboBox(box4)
        self.func_box4.currentTextChanged.connect(self.box_cicked)

        self.names = [QPushButton(i) if i else None for i in names]

        for i, j in enumerate(self.names):
            if j is not None:
                j.clicked.connect(self.button_clicked)
                self.glayout.addWidget(j, i//5+1, i % 5)
        last = len(self.names)-1

        self.ok_button = QPushButton(tras("Yes"), self)
        self.ok_button.clicked.connect(self.check)

        self.debug_line = LineEdit()
        self.debug_line.setReadOnly(True)

        self.glayout.addWidget(self.func_box1, 1, 0)
        self.glayout.addWidget(self.func_box2, 1, 1)
        self.glayout.addWidget(self.func_box3, 1, 2)
        self.glayout.addWidget(self.func_box4, 1, 3)
        self.glayout.addWidget(self.ok_button, last//5+1, last % 5)
        self.glayout.addWidget(self.debug_line, last//5+2, 0, 1, 5)

        self.resize(self.sizeHint())

    def box_cicked(self, text: str):
        """
        combobox点击事件
        """
        box: ComboBox = self.sender()
        box.setCurrentIndex(0)
        if text != box.list.item(0).text():
            self.add_func(text)
        self.display.setFocus()

    def button_clicked(self):
        """
        button点击事件
        """
        text = self.sender().text()
        if text == "Back":
            self.display.back()
        else:
            self.add_func(self.sender().text())
        self.display.setFocus()

    def add_func(self, text: str):
        """
        添加函数文本
        """
        pos = self.display.cursorPosition()
        func = self.display.text()
        func = func[:pos] + text + func[pos:]
        self.display.setText(func)
        self.display.setCursorPosition(pos+len(text))

    def change_xy(self, text: str):
        """
        实时改变x/y按钮的文字
        """
        if text == "f(x)=":
            self.names[-2].setText("x")
        elif text == "f(y)=":
            self.names[-2].setText("y")
        else:
            self.names[-2].setText("")

    def check(self):
        """
        检查提交的函数解析式，并发送给plotwidget
        """
        dic = {}
        if (text := self.display.text()):
            dic["FuncType"] = self.func_type.currentText()
            dic["FuncName"] = text
            self.signal.emit(dic)
            self.display.his_list.append(text)
            self.display.his_pos = len(self.display.his_list)-1

    def keyPressEvent(self, event: QKeyEvent) -> None:
        """
        重写QT按键事件
        """
        if event.key() in [Qt.Key.Key_Return, Qt.Key.Key_Enter]:
            self.check()
