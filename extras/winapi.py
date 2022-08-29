"""
Windows API functions.
"""

from ctypes import windll, c_ulong, create_string_buffer, create_unicode_buffer, byref
from ctypes import wintypes
from codecs import decode


user32 = windll.user32
kernel32 = windll.kernel32
psapi = windll.psapi

ABOVE_NORMAL_PRIORITY_CLASS=0x00008000

HIGH_PRIORITY_CLASS=0x00000080

NORMAL_PRIORITY_CLASS=0x00000020


def GetForegroundWindow() -> wintypes.HWND:
    """
    Get the HWND of the current foreground window.
    """
    return windll.user32.GetForegroundWindow()


def GetWindowThreadProcessId(hwnd) -> list[wintypes.DWORD, wintypes.LPDWORD]:
    """
    Get the Thread ID and Process of a given HWND.
    """
    pid = c_ulong()
    tid = windll.user32.GetWindowThreadProcessId(hwnd, byref(pid))
    return tid, pid.value


def GetWindowText(hwnd):
    length = user32.GetWindowTextLengthW(hwnd)
    buff = create_unicode_buffer(length)
    user32.GetWindowTextW(hwnd, buff, length + 1)
    text = str(buff.value).strip()
    if len(text) != 0:
        return text


def GetModuleFileName(pid) -> str:
    """
    Get the filename of the module that contains the given HWND.
    """
    handle = OpenProcess(pid)
    buff = create_string_buffer(b'', wintypes.MAX_PATH)
    psapi.GetModuleFileNameExA(handle, None, buff, wintypes.MAX_PATH)
    kernel32.CloseHandle(handle)
    exe = str(decode(buff.value, 'utf-8')).strip()
    if len(exe) != 0:
        return exe

def OpenProcess(pid) -> wintypes.HANDLE:
    """
    Open a handle to the given process.
    """
    return kernel32.OpenProcess(0x001F0FFF, False, pid)

def GetPriorityClass(pid):
    """
    Get the priority class of the given process.
    """
    handle = OpenProcess(pid)
    priority_class = kernel32.GetPriorityClass(handle)
    kernel32.CloseHandle(handle)
    if priority_class == 0:
        return None
    else:
        return hex(priority_class)

def SetPriorityClass(pid, priority_class):
    """
    Set the priority class of the given process.
    """
    handle = OpenProcess(pid)
    kernel32.SetPriorityClass(handle, priority_class)
    kernel32.CloseHandle(handle)