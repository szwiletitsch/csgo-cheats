import win32api
import win32gui
import win32process
import pymem

from vector import Vec3


def get_handle_and_open_process_by_name(window_name: str):
    window_handle = win32gui.FindWindow(0, window_name)
    if window_handle:
        pid = win32process.GetWindowThreadProcessId(window_handle)
        handle = pymem.Pymem()
        handle.open_process_from_id(pid[1])
        return handle
    else:
        exit("CSGO wasn't found")


def get_module(name, handle):
    list_of_modules = handle.list_modules()
    while list_of_modules is not None:
        tmp = next(list_of_modules)
        print(tmp)
        if tmp[0].name == name:
            client_dll = tmp[1]
            return client_dll
    exit("module not found")


def read_vec(handle, location):
    return Vec3(handle.read_float(location), handle.read_float(location + 4), handle.read_float(location + 8))


def write_vec(handle, location, xyz):
    handle.write_float(location, float(xyz[0]))
    handle.write_float(location + 4, float(xyz[1]))
    handle.write_float(location + 8, float(xyz[2]))


def is_pressed(key):
    if win32api.GetKeyState(key) == -128 or win32api.GetKeyState(key) == -127:
        return True
    return False


