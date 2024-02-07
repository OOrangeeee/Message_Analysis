from ctypes import WinDLL


def no_con():
    kernel32 = WinDLL("kernel32")
    user32 = WinDLL("user32")
    HWND = kernel32.GetConsoleWindow()
    if HWND != 0:
        user32.ShowWindow(HWND, 0)
