# coding:utf-8
import sys
from PySide6.QtCore import Qt, QPointF, QSize, QEvent
from PySide6.QtGui import QColor, QIcon, QPainter, QPainterPath, QPen
from PySide6.QtWidgets import QHBoxLayout, QWidget, QToolButton
from .utils import startSystemMove


class TitleBarButton(QToolButton):
    """ Title bar button """

    def __init__(self, style=None, parent=None):
        """
        Parameters
        ----------
        style: dict
            button style of `normal`,`hover`, and `pressed`. Each state has
            `color`, `background` and `icon`(close button only) attributes.

        parent:
            parent widget
        """
        super().__init__(parent)
        self.setCursor(Qt.CursorShape.ArrowCursor)
        self.setFixedSize(46, 32)
        self._state = "normal"
        self._style = {
            "normal": {
                "color": (0, 0, 0, 255),
                "background": (0, 0, 0, 0)
            },
            "hover": {
                "color": (255, 255, 255),
                # "background": (0, 100, 182)
                "background": (55, 55, 55)
            },
            "pressed": {
                "color": (255, 255, 255),
                "background": (54, 57, 65)
            },
        }
        self.updateStyle(style)
        self.setStyleSheet("""
            QToolButton{
                background-color: transparent;
                border: none;
                margin: 0px;
            }
        """)

    def updateStyle(self, style):
        """ update the style of button

        Parameters
        ----------
        style: dict
            button style of `normal`,`hover`, and `pressed`. Each state has
            `color`, `background` and `icon`(close button only) attributes.
        """
        style = style or {}
        for k, v in style.items():
            self._style[k].update(v)

        self.update()

    def setState(self, state):
        """ set the state of button

        Parameters
        ----------
        state: str
            the state of button, can be `normal`,`hover`, or `pressed`
        """
        if state not in ("normal", "hover", "pressed"):
            raise ValueError("The state can only be `normal`,`hover`, or `pressed`")

        self._state = state
        self.update()

    def enterEvent(self, e):
        self.setState("hover")
        super().enterEvent(e)

    def leaveEvent(self, e):
        self.setState("normal")
        super().leaveEvent(e)

    def mousePressEvent(self, e):
        if e.button() != Qt.MouseButton.LeftButton:
            return

        self.setState("pressed")
        super().mousePressEvent(e)


class MinimizeButton(TitleBarButton):
    """ Minimize button """

    def paintEvent(self, e):
        painter = QPainter(self)

        # draw background
        style = self._style[self._state]
        painter.setBrush(QColor(*style["background"]))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRect(self.rect())

        # draw icon
        painter.setBrush(Qt.BrushStyle.NoBrush)
        pen = QPen(QColor(*style["color"]), 1)
        pen.setCosmetic(True)
        painter.setPen(pen)
        painter.drawLine(18, 16, 28, 16)


class MaximizeButton(TitleBarButton):
    """ Maximize button """

    def __init__(self, style=None, parent=None):
        super().__init__(style, parent)
        self.__isMax = False

    def setMaxState(self, isMax):
        """ update the maximized state and icon """
        if self.__isMax == isMax:
            return

        self.__isMax = isMax
        self.setState("normal")

    def paintEvent(self, e):
        painter = QPainter(self)

        # draw background
        style = self._style[self._state]
        painter.setBrush(QColor(*style["background"]))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRect(self.rect())

        # draw icon
        painter.setBrush(Qt.BrushStyle.NoBrush)
        pen = QPen(QColor(*style["color"]), 1)
        pen.setCosmetic(True)
        painter.setPen(pen)

        r = self.devicePixelRatioF()
        painter.scale(1/r, 1/r)
        if not self.__isMax:
            painter.drawRect(int(18*r), int(11*r), int(10*r), int(10*r))
        else:
            painter.drawRect(int(18*r), int(13*r), int(8*r), int(8*r))
            x0 = int(18*r)+int(2*r)
            y0 = 13*r
            dw = int(2*r)
            path = QPainterPath(QPointF(x0, y0))
            path.lineTo(x0, y0-dw)
            path.lineTo(x0+8*r, y0-dw)
            path.lineTo(x0+8*r, y0-dw+8*r)
            path.lineTo(x0+8*r-dw, y0-dw+8*r)
            painter.drawPath(path)


class CloseButton(TitleBarButton):
    """ Close button """

    def __init__(self, style=None, parent=None):
        defaultStyle = {
            "normal": {
                "background": (0, 0, 0, 0),
                "icon": "./widgets/resource/title_bar/close_black.svg"
            },
            "hover": {
                "background": (232, 17, 35),
                "icon": "./widgets/resource/title_bar/close_white.svg"
            },
            "pressed": {
                "background": (241, 112, 122),
                "icon": "./widgets/resource/title_bar/close_white.svg"
            },
        }
        super().__init__(defaultStyle, parent)
        self.updateStyle(style)
        self.setIconSize(QSize(46, 32))
        self.setIcon(QIcon(self._style["normal"]["icon"]))

    def updateStyle(self, style):
        super().updateStyle(style)
        self.setIcon(QIcon(self._style[self._state]["icon"]))

    def enterEvent(self, e):
        self.setIcon(QIcon(self._style["hover"]["icon"]))
        super().enterEvent(e)

    def leaveEvent(self, e):
        self.setIcon(QIcon(self._style["normal"]["icon"]))
        super().leaveEvent(e)

    def mousePressEvent(self, e):
        self.setIcon(QIcon(self._style["pressed"]["icon"]))
        super().mousePressEvent(e)

    def mouseReleaseEvent(self, e):
        self.setIcon(QIcon(self._style["normal"]["icon"]))
        super().mouseReleaseEvent(e)

    def paintEvent(self, e):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # draw background
        style = self._style[self._state]
        painter.setBrush(QColor(*style["background"]))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRect(self.rect())

        # draw icon
        super().paintEvent(e)


class TitleBar(QWidget):
    """ Title bar """

    def __init__(self, parent):
        super().__init__(parent)
        self.minBtn = MinimizeButton(parent=self)
        self.closeBtn = CloseButton(parent=self)
        self.maxBtn = MaximizeButton(parent=self)
        self.hBoxLayout = QHBoxLayout(self)

        # self.resize(200, 32)
        self.setFixedHeight(32)

        # add buttons to layout
        self.hBoxLayout.setSpacing(0)
        self.hBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.hBoxLayout.addWidget(self.minBtn, 0, Qt.AlignmentFlag.AlignRight)
        self.hBoxLayout.addWidget(self.maxBtn, 0, Qt.AlignmentFlag.AlignRight)
        self.hBoxLayout.addWidget(self.closeBtn, 0, Qt.AlignmentFlag.AlignRight)
        self.hBoxLayout.setAlignment(Qt.AlignRight)

        # connect signal to slot
        self.minBtn.clicked.connect(self.window().showMinimized)
        self.maxBtn.clicked.connect(self.__toggleMaxState)
        self.closeBtn.clicked.connect(self.window().close)

        self.window().installEventFilter(self)

    def eventFilter(self, obj, e):
        if obj is self.window():
            if e.type() == QEvent.Type.WindowStateChange:
                self.maxBtn.setMaxState(self.window().isMaximized())
                return False

        return super().eventFilter(obj, e)

    def mouseDoubleClickEvent(self, event):
        """ Toggles the maximization state of the window """
        if event.button() != Qt.MouseButton.LeftButton:
            return

        self.__toggleMaxState()

    def mouseMoveEvent(self, e):
        if sys.platform != "win32" or not self._isDragRegion(e.pos()):
            return

        startSystemMove(self.window(), e.globalPos())

    def __toggleMaxState(self):
        """ Toggles the maximization state of the window and change icon """
        if self.window().isMaximized():
            self.window().showNormal()
        else:
            self.window().showMaximized()

    def _isDragRegion(self, pos):
        """ Check whether the pressed point belongs to the area where dragging is allowed """
        return 0 < pos.x() < self.width() - 46 * 3
