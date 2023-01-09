"""
设置窗口效果
"""
# pylint: disable=no-name-in-module
import sys
import darkdetect
from PySide6.QtGui import Qt
from PySide6.QtWidgets import QWidget
from setting import settings


def set_effect(widget: QWidget):
    """
    设置窗口效果
    """
    if (window_effect := settings["Window-Effect"]) != "Default":
        widget.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        widget.setStyleSheet("background:transparent")
    if window_effect == "Mica":
        mode = darkdetect.theme() == "Dark"
        if sys.getwindowsversion().build > 22000:
            import win32mica
            win32mica.ApplyMica(widget.winId(), mode)
        else:
            widget.setAttribute(
                Qt.WidgetAttribute.WA_TranslucentBackground, False)
    elif window_effect == "Acrylic":
        from BlurWindow.blurWindow import GlobalBlur
        GlobalBlur(widget.winId(), Dark=True)
