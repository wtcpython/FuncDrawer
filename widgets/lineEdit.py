# coding:utf-8
from PySide6.QtCore import (QEasingCurve, QPropertyAnimation, QRect,
                            Qt, QPoint)
from PySide6.QtGui import (QAction, QContextMenuEvent, QIcon)
from PySide6.QtWidgets import QApplication, QLineEdit, QMenu


class LineEdit(QLineEdit):
    """ 包含清空按钮的单行输入框 """

    def __init__(self, text=None, parent=None):
        super().__init__(text, parent)
        self.setClearButtonEnabled(True)
        self.menu = LineEditMenu(self)
        self.__clickedTime = 0
        # # 设置层叠样式
        # with open('widgets/resource/style/line_edit.qss',
        #           encoding='utf-8') as f:
        #     self.setStyleSheet(f.read())

    def mousePressEvent(self, e):
        if e.button() == Qt.MouseButton.LeftButton:
            # 如果已经全选了再次点击就取消全选
            if self.__clickedTime == 0:
                self.selectAll()
            else:
                # 需要调用父类的鼠标点击事件，不然无法部分选中
                super().mousePressEvent(e)
            self.setFocus()
        self.__clickedTime += 1

    def contextMenuEvent(self, event: QContextMenuEvent):
        """ 设置右击菜单 """
        self.menu.exec_(event.globalPos())


class LineEditMenu(QMenu):
    """ 单行输入框右击菜单 """

    def __init__(self, parent):
        super().__init__("", parent)
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.Popup | Qt.WindowType.NoDropShadowWindowHint
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        # 不能直接改width
        self.animation = QPropertyAnimation(self, b"geometry")
        self.animation.setDuration(300)
        self.animation.setEasingCurve(QEasingCurve.Type.OutQuad)

    def createActions(self):
        # 创建动作
        self.cutAct = QAction(
            QIcon("widgets/resource/images/剪切.png"),
            "剪切",
            self,
            shortcut="Ctrl+X",
            triggered=self.parent().cut,
        )
        self.copyAct = QAction(
            QIcon("widgets/resource/images/复制.png"),
            "复制",
            self,
            shortcut="Ctrl+C",
            triggered=self.parent().copy,
        )
        self.pasteAct = QAction(
            QIcon("widgets/resource/images/粘贴.png"),
            "粘贴",
            self,
            shortcut="Ctrl+V",
            triggered=self.parent().paste,
        )
        self.cancelAct = QAction(
            QIcon("widgets/resource/images/撤销.png"),
            "取消操作",
            self,
            shortcut="Ctrl+Z",
            triggered=self.parent().undo,
        )
        self.selectAllAct = QAction(
            "全选", self, shortcut="Ctrl+A", triggered=self.parent().selectAll
        )
        # 创建动作列表
        self.action_list = [
            self.cutAct,
            self.copyAct,
            self.pasteAct,
            self.cancelAct,
            self.selectAllAct,
        ]

    def exec_(self, pos: QPoint):
        # 删除所有动作
        self.clear()
        # clear之后之前的动作已不再存在故需重新创建
        self.createActions()
        # 初始化属性
        self.setProperty("hasCancelAct", "false")
        width = 176
        actionNum = len(self.action_list)
        # 访问系统剪贴板
        self.clipboard = QApplication.clipboard()
        # 根据剪贴板内容是否为text分两种情况讨论
        if self.clipboard.mimeData().hasText():
            # 再根据3种情况分类讨论
            if self.parent().text():
                self.setProperty("hasCancelAct", "true")
                width = 213
                if self.parent().selectedText():
                    self.addActions(self.action_list)
                else:
                    self.addActions(self.action_list[2:])
                    actionNum -= 2
            else:
                self.addAction(self.pasteAct)
                actionNum = 1
        else:
            if self.parent().text():
                self.setProperty("hasCancelAct", "true")
                width = 213
                if self.parent().selectedText():
                    self.addActions(
                        self.action_list[:2] + self.action_list[3:])
                    actionNum -= 1
                else:
                    self.addActions(self.action_list[3:])
                    actionNum -= 3
            else:
                return
        # 每个item的高度为38px，10为上下的内边距和
        height = actionNum * 36 + 5
        # 不能把初始的宽度设置为0px，不然会报警
        self.animation.setStartValue(QRect(pos.x(), pos.y(), 1, 1))
        self.animation.setEndValue(QRect(pos.x(), pos.y(), width, height))
        self.setStyle(QApplication.style())
        # 开始动画
        self.animation.start()
        super().exec_(pos)
