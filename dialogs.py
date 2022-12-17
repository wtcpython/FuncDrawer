"""
    对话框主文件
"""
# pylint: disable=no-name-in-module
from setting import ComboBox
from translate import tras
from PySide6.QtCore import Signal
from PySide6.QtGui import Qt, QKeyEvent
from PySide6.QtWidgets import QPushButton, QGridLayout, QLineEdit, QWidget
from widgets import LineEdit


names = ["", "", "", "", "Back",
         "round(", "(", ")", "absolute(", "sqrt(",
         "7", "8", "9", "**", "%",
         "4", "5", "6", "*", "/",
         "1", "2", "3", "+", "-",
         "0", ".", ",", "x", ""]
box1 = [tras("三角"), "sin(", "cos(", "tan(", "sinh(", "cosh(", "tanh("]
box2 = [tras("反三角"), "arcsin(", "arccos(", "arctan(",
        "arcsinh(", "arccosh(", "arctanh("]
box3 = [tras("对数"), "log(", "lg(", "ln(", "sqrt(", "abs("]
box4 = [tras("常数"), "e", "pi"]
STRING = "".join(set(names[5:-1]+box1+box2+box3+box4))


class FuncLineEdit(QLineEdit):
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
        if key in [Qt.Key.Key_Left, Qt.Key.Key_Right, Qt.Key.Key_Backspace]:
            super().keyPressEvent(event)

        elif key == Qt.Key.Key_Up:
            if self.his_list and self.his_pos > 0:
                self.setText(self.his_list[self.his_pos])
                self.his_pos -= 1

        elif key == Qt.Key.Key_Down:
            if self.his_list and self.his_pos < len(self.his_list)-1:
                self.setText(self.his_list[self.his_pos])
                self.his_pos += 1

        elif text in STRING:
            super().keyPressEvent(event)
            if text == "(":
                pos = self.cursorPosition()
                txt = self.text()
                self.setText(txt[:pos]+")"+txt[pos:])
                self.setCursorPosition(pos)


class FuncDialog(QWidget):
    """
    绘制函数的对话框
    """

    signal = Signal(dict)

    def __init__(self):
        super().__init__()
        self.setWindowTitle(tras("Func Drawer"))
        self.signal.emit({})

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

        self.debug_line = QLineEdit(self)
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

    def button_clicked(self):
        """
        button点击事件
        """
        text = self.sender().text()
        if text == "Back":
            self.display.back()
        else:
            self.add_func(self.sender().text())

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
