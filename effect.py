"""
设置窗口效果
"""
import sys
if sys.getwindowsversion().build > 22000:
    import win32mica
    set_effect = win32mica.ApplyMica
else:
    from BlurWindow.blurWindow import GlobalBlur

    def set_effect(hwnd, mode):
        """
        设置窗口效果
        """
        GlobalBlur(hwnd, Dark=mode)
