"""
设置窗口效果
"""
# pylint: disable=no-name-in-module
import sys
import darkdetect
from PySide6.QtGui import Qt
from PySide6.QtWidgets import QWidget
from setting import settings

STYLE = ""
if (effect := settings["Window-Effect"]) == "Follow System":
    mode = darkdetect.theme() == "Dark"
else:
    mode = effect


BORDER_RADIUS = "border-radius: 10px;"

BKG_CLR = "background: rgba(240, 240, 240, 0);"
if mode:
    BKG_CLR = "background: rgba(32, 32, 32, 0);"
BKG_CLR2 = "background: rgba(240, 240, 240, 0);"
if mode:
    BKG_CLR2 = "background: rgba(32, 32, 32, 0);"
BKG_CLR_HOVER = "background: rgb(230, 230, 230);"
if mode:
    BKG_CLR_HOVER = "background: rgb(63, 63, 63);"

BKG_CLR3 = "background: rgb(220, 220, 220);"
if mode:
    BKG_CLR3 = "background: rgb(96, 96, 96);"

color = (0, 0, 0)
if mode:
    color = (255, 255, 255)

GLOBAL = f"""
    *{{
        font: {settings['Font-Size']}px {settings['Font']};
        color: rgb{color};
        {BKG_CLR}
        border: none;
    }}
    """
STYLE += GLOBAL

TABBAR = f"""
    QTabWidget::tab-bar{{
        left: 10px;
        margin: 5px;
    }}

    QTabBar::tab{{
        margin-left: 2px;
        margin-top: 5px;
        padding: 5px;
        min-width: 40px;
        height: 20px;
        {BORDER_RADIUS}
    }}

    QTabBar::tab:selected{{
        {BKG_CLR_HOVER}
    }}
    """
STYLE += TABBAR

MENUBAR = f"""
    QMenuBar::item{{
        padding: 5px;
    }}

    QMenuBar::item:selected{{
        {BKG_CLR_HOVER}
        {BORDER_RADIUS}
    }}
    """
STYLE += MENUBAR

MENU = f"""
    QMenu{{
        {BKG_CLR3}
        margin: 0px;
        padding: 5px 0px 5px 0px;
        {BORDER_RADIUS}
    }}

    QMenu::separator{{
        height: 1px;
        width: 140px;
        background: rgba(0, 0, 0, 104);
        margin-right: 13px;
        margin-top: 5px;
        margin-bottom: 5px;
        margin-left: 13;
    }}

    QMenu::item{{
        padding: 4px 28px 4px 28px;
        {BORDER_RADIUS}
    }}

    QMenu::item:selected{{
        border: 1px rgb(212, 212, 212);
        background: rgba(0, 0, 0, 25);
        color: black;
    }}

    QMenu::right-arrow{{
        width: 16px;
        height: 16px;
        right: 16px;
    }}
    """
STYLE += MENU

LINEEDIT = f"""
    QLineEdit{{
        height: 32px;
        {BKG_CLR_HOVER}
        {BORDER_RADIUS}
        padding-left: 5px;
    }}

    QLineEdit:focus{{
        {BKG_CLR}
    }}
    """
STYLE += LINEEDIT

LISTWIDGET = f"""
    QListWidget{{
        outline: none;
        {BKG_CLR2}
    }}

    QListWidget::item{{
        height: 25px;
        border-radius: 5px;
    }}

    QListWidget::item:hover,
    QListWidget::item:selected{{
        {BKG_CLR_HOVER}
        color: black;
    }}
    """
STYLE += LISTWIDGET

PUSHBUTTON = f"""
    QPushButton{{
        {BKG_CLR3}
        {BORDER_RADIUS}
        padding: 5px;
    }}

    QPushButton::hover{{
        {BKG_CLR_HOVER}
    }}
    """
STYLE += PUSHBUTTON

OTHER = f"""
    QToolTip{{
        padding: 5px;
        {BKG_CLR_HOVER}
        {BORDER_RADIUS}
    }}

    QComboBox{{
        padding: 5px;
        {BKG_CLR3}
        {BORDER_RADIUS}
    }}

    #ComboBoxView{{
        {BKG_CLR3}
        {BORDER_RADIUS}
    }}

    #SettingWidget{{
        {BKG_CLR_HOVER}
        {BORDER_RADIUS}
    }}

    #Label{{
        {BKG_CLR_HOVER}
    }}
    """

STYLE += OTHER


def set_effect(app: QWidget | None, widget: QWidget):
    """
    设置窗口效果
    """
    if app:
        app.setStyleSheet(STYLE)

    if sys.getwindowsversion().build > 22000:
        import win32mica
        win32mica.ApplyMica(widget.winId(), mode)

    else:
        widget.setAttribute(
                Qt.WidgetAttribute.WA_TranslucentBackground, False)
