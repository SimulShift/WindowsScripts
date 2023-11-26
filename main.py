import pygetwindow as gw
# Press Ctrl+F5 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
# Press the green button in the gutter to run the script.

def list_open_windows():
    for window in gw.getAllWindows():
        print(window.title)

if __name__ == '__main__':
    list_open_windows()
    pass

