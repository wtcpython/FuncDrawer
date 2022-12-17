from PySide6.QtWidgets import QWidget
from widgets import WindowEffect


def setMicaEffect(widget: QWidget, dark: bool = False):
    effect = WindowEffect(widget)
    effect.setMicaEffect(widget.winId(), dark)
