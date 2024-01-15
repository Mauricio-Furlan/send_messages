import tkinter as tk
from PIL import ImageGrab, Image, ImageDraw, ImageTk
import pyautogui
import keyboard
x_start, y_start, x_end, y_end = 0, 0, 0, 0
drawing = False
keyboard.wait('h')
def on_move(event):
    global x_end, y_end, drawing

    if drawing:
        x_end, y_end = event.x_root, event.y_root
        draw_rectangle()

def draw_rectangle():
    screen_captured = ImageGrab.grab()
    mask = Image.new('L', screen_captured.size, 50)
    draw = ImageDraw.Draw(mask)
    draw.rectangle([x_start, y_start, x_end, y_end], fill=255)
    alpha = Image.new('L', screen_captured.size, 100)
    alpha.paste(mask, (0, 0), mask=mask)

    img = Image.composite(screen_captured, Image.new('RGB', screen_captured.size, 'white'), alpha)

    img_tk = ImageTk.PhotoImage(img)
    canvas.create_image(0, 0, image=img_tk, anchor=tk.NW)
    canvas.img_tk = img_tk

def on_click(event):
    global x_start, y_start, drawing

    x_start, y_start = event.x_root, event.y_root
    drawing = True

def finalizar_programa():
    global x_start, y_start, x_end, y_end
    x1, y1 = min(x_start, x_end), min(y_start, y_end)
    x2, y2 = max(x_start, x_end), max(y_start, y_end)
    width = x2 - x1
    height = y2 - y1
    value = {
        'left': x1,
        'top': y1,
        'width': width,
        'height': height
    }
    print(value)

    root.withdraw()
    img = pyautogui.screenshot(region=(x1, y1, width, height))
    img.save('image.png')
    root.deiconify() 

    root.quit()
def on_release(_):
    global drawing

    drawing = False
    finalizar_programa()

root = tk.Tk()
root.overrideredirect(True) 
root.attributes('-topmost', True) 
root.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(), root.winfo_screenheight())) 
root.attributes('-alpha', 0.5)  

canvas = tk.Canvas(root, width=root.winfo_screenwidth(), height=root.winfo_screenheight(),  highlightthickness=0)
canvas.pack()

canvas.bind("<B1-Motion>", on_move)
canvas.bind("<ButtonPress-1>", on_click)
canvas.bind("<ButtonRelease-1>", on_release)

root.mainloop()