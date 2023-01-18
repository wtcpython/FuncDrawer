"""
设置窗口效果
"""
# pylint: disable=no-name-in-module
import sys
import darkdetect
from PySide6.QtGui import Qt
from PySide6.QtWidgets import QWidget
from setting import settings
from translate import tmp_path

with open(tmp_path/"style.qss", encoding="UTF-8") as file:
    style = file.read()
style += f"*{'{'}font:{settings['Font-Size']}px '{settings['Font']}'{'}'}"

if settings["Window-Effect"] != "Default":
    style += "*{background:rgba(255,255,255,0)}"


def set_effect(app: QWidget | None, widget: QWidget):
    """
    设置窗口效果
    """
    if (window_effect := settings["Window-Effect"]) != "Default":
        widget.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
    if app:
        app.setStyleSheet(style)
    mode = darkdetect.theme() == "Dark"
    if window_effect == "Mica":
        if sys.getwindowsversion().build > 22000:
            import win32mica
            win32mica.ApplyMica(widget.winId(), mode)
        else:
            widget.setAttribute(
                Qt.WidgetAttribute.WA_TranslucentBackground, False)
    else:
        from BlurWindow.blurWindow import GlobalBlur
        if window_effect == "Acrylic":
            GlobalBlur(widget.winId(), Acrylic=True, Dark=mode)
        elif window_effect == "Aero":
            GlobalBlur(widget.winId(), Dark=mode)
