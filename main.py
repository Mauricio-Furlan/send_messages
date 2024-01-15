import ctypes
import time
import keyboard
import pyautogui
from screen import find_image, look_screen
import cv2

WM_KEYDOWN = 0x0100
WM_KEYUP = 0x0101
WM_MOUSEMOVE = 0x0200
MK_LBUTTON = 0x0001

WM_LBUTTONDOWN = 0x0201
WM_LBUTTONUP = 0x0202
WM_RBUTTONDOWN = 0x0204
WM_RBUTTONUP = 0x0205


F1 = 0x70
F2 = 0x71
F3 = 0x72
F4 = 0x73
F5 = 0x74
F6 = 0x75
F7 = 0x76
F8 = 0x77
F9 = 0x78
F10 = 0x79
F11 = 0x7A
F12 = 0x7B 

SCAN_F1= 0x3B
SCAN_F2= 0x3C
SCAN_F3= 0x3D
SCAN_F4= 0x3E
SCAN_F5= 0x3F
SCAN_F6= 0x40
SCAN_F7= 0x41
SCAN_F8= 0x42
SCAN_F9= 0x43
SCAN_F10= 0x44
SCAN_F11= 0x57
SCAN_F12= 0x58
SCAN_ENTER= 0x1C
SCAN_CTROL= 0x1D
SCAN_BACKSPACE= 0x0E
SCAN_CAPS= 0x3A
SCAN_NUNLOCK= 0x45
SCAN_TAB= 0x0F
SCAN_UP = 0xC8
SCAN_LEFT = 0xCB
SCAN_RIGHT = 0xCD
SCAN_DOWN = 0xD0
SCAN_ENTER = 0x1C
SCAN_ESC = 0x01

# funciona no tibia, otpokemon, pokemon doido
# nao funciona no pxg
def send_message_keyboard(hwnd, key_code):
    ctypes.windll.user32.SendMessageW(hwnd, WM_KEYDOWN, key_code, 0)
    time.sleep(0.2)
    ctypes.windll.user32.SendMessageW(hwnd, WM_KEYUP, key_code, 0)

hwnd = ctypes.windll.user32.FindWindowW(0, 'Tibia - Closefriends')

def send_key_to_window(hwnd, scan_code):
    lParam_down = (1 << 0) | (scan_code << 16)
    lParam_up = (1 << 0) | (scan_code << 16) | (1 << 30) | (1 << 31)
    ctypes.windll.user32.SendMessageW(hwnd, WM_KEYDOWN, scan_code, lParam_down)
    time.sleep(0.2)
    ctypes.windll.user32.SendMessageW(hwnd, WM_KEYUP, scan_code, lParam_up)

def moveTo(hwnd, x, y):
    x = int(x)
    y = int(y)
    lParam = (y << 16) | x
    ctypes.windll.user32.PostMessageW(hwnd, WM_MOUSEMOVE, MK_LBUTTON, lParam)

def click(hwnd, x, y, button='left'):
    x = int(x)
    y = int(y)
    lParam = (y << 16) | x
    if button == 'left':
        ctypes.windll.user32.SendMessageW(hwnd, WM_LBUTTONDOWN, 1, lParam)
        time.sleep(0.015)
        ctypes.windll.user32.SendMessageW(hwnd, WM_LBUTTONUP, 0, lParam)
        return
    ctypes.windll.user32.SendMessageW(hwnd, WM_RBUTTONDOWN, 0, lParam)
    time.sleep(0.015)
    ctypes.windll.user32.SendMessageW(hwnd, WM_RBUTTONUP, 0, lParam)

keyboard.wait('h')
img = look_screen()
result = find_image(img, 'image.png')
print('result', result)
# if result:
#     moveTo(hwnd, result[0], result[1])
#     click(hwnd, result[0], result[1], 'right')

# cv2.imshow('test', img)
# cv2.waitKey(0)
# while True:
#     print('esperando...')
#     time.sleep(15)
#     print('usando magia...')
#     send_message_keyboard(hwnd, F3)
#     print('comendo comida...')
#     send_message_keyboard(hwnd, F6)