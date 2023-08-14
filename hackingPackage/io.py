import win32api


def is_pressed(key):
    if win32api.GetKeyState(key) == -128 or win32api.GetKeyState(key) == -127:
        return True
    return False
