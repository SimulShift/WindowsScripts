import subprocess
import os
from time import sleep

import pygetwindow as gw
import win32gui
import win32con
from win10toast import ToastNotifier

url = "https://chat.openai.com"
chrome_path = "C:/Program Files/Google/Chrome/Application/chrome.exe"
width = 1200  # Set the desired window width
height = 1000  # Set the desired window height
app = f'data:text/html,<html><body><script>window.moveTo(580,240);window.resizeTo({width},{height});window.location=\'{url}\';</script></body></html>'
hwnd_file = 'hwnd.txt'

# Ensure the path to Chrome is correct and exists
if not os.path.isfile(chrome_path):
    raise Exception(f"The specified Chrome path does not exist: {chrome_path}")

def open_chrome_app():
    subprocess.run([chrome_path, f'--app={app}', f'--profile-directory=Default'])

def save_hwnd_to_file(hWnd, file_path):
    with open(file_path, 'w') as f:
        f.write(str(hWnd))

def get_hwnd_from_file(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            hwnd = f.read()
            if hwnd == 'None':
                return -1
            return int(hwnd)
    return None

def find_chrome_app_window():
    for window in gw.getWindowsWithTitle(''):
        if "ChatGPT" in window.title:
            return window._hWnd
    return None

def show_toast_with_message(message):
    toaster = ToastNotifier()
    toaster.show_toast("OpenAI ChatGPT", message, duration=5, threaded=True)

def bring_to_foreground(hWnd):
    if win32gui.IsIconic(hWnd):
        win32gui.ShowWindow(hWnd, win32con.SW_RESTORE)
    win32gui.SetForegroundWindow(hWnd)

def check_if_chrome_app_is_running(hwnd):
    for window in gw.getAllWindows():
        # print window title and their hwnd
        print(f'window: {window.title}, hwnd: {window._hWnd}')
        if window._hWnd == hwnd:
            return window
    return None

def minimize_window(hWnd):
    win32gui.ShowWindow(hWnd, win32con.SW_MINIMIZE)

def is_window_minimized(hWnd):
    placement = win32gui.GetWindowPlacement(hWnd)
    print(f'placement: {placement}')
    return placement[1] == win32con.SW_SHOWMINIMIZED

hwnd = get_hwnd_from_file(hwnd_file)
#show_toast_with_message(f'hwnd: {hwnd} os.getcwd: {os.getcwd()}')
print(f'looking for hwnd: {hwnd}')
window = check_if_chrome_app_is_running(hwnd)
if window is not None:
    print("Chrome app is already running")
    # check if it's in the foreground
    if not is_window_minimized(hwnd):
        print("Chrome app is in the foreground")
        minimize_window(hwnd)
    else:
        window.activate()
        bring_to_foreground(hwnd)
else:
    print("Chrome app is not running")
    show_toast_with_message("Chrome app is not running")
    open_chrome_app()
    # wait for the window to appear
    retries = 10
    hwnd = None
    while hwnd is None and retries > 0:
        print(f'retries: {retries}')
        hwnd = find_chrome_app_window()
        if hwnd is not None:
            print(f'found hwnd: {hwnd}')
            break
        sleep(1)
        retries -= 1
        if retries == 0:
            show_toast_with_message("Retry limit reached. Exiting.")
    save_hwnd_to_file(hwnd, hwnd_file)
