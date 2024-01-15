import numpy as np
from ctypes import windll
import win32gui
import win32ui
import cv2


WINDOW_TITLE = "Projetor em janela (fonte) - Captura de jogo"
HWND = win32gui.FindWindow(None, WINDOW_TITLE)
print('HWND ->', HWND)

class WindowScreenshot:
    def __init__(self):
        self.hwnd_dc = None
        self.mfc_dc = None
        self.save_dc = None
        self.bitmap = None
        self.result = None
        self.bmpinfo = None
        self.bmpstr = None
        self._valid_dc = False

    def __enter__(self):
        if win32gui.IsWindow(HWND):
            self.hwnd_dc = win32gui.GetWindowDC(HWND)
            if self.hwnd_dc != 0:
                try:
                    left, top, right, bottom = win32gui.GetClientRect(HWND)
                    w = right - left
                    h = bottom - top
                    self.mfc_dc = win32ui.CreateDCFromHandle(self.hwnd_dc)
                    self.save_dc = self.mfc_dc.CreateCompatibleDC()
                    self.bitmap = win32ui.CreateBitmap()
                    self.bitmap.CreateCompatibleBitmap(self.mfc_dc, w, h)
                    self.save_dc.SelectObject(self.bitmap)
                    self.result = windll.user32.PrintWindow(HWND, self.save_dc.GetSafeHdc(), 3)
                    self.bmpinfo = self.bitmap.GetInfo()
                    self.bmpstr = self.bitmap.GetBitmapBits(True)

                    self._valid_dc = True
                except win32ui.error as e:
                    win32gui.ReleaseDC(HWND, self.hwnd_dc)
                    self.mfc_dc = None
                    self._valid_dc = False
            else:
                print('Error HWND_DC is 0')
                win32gui.ReleaseDC(HWND, self.hwnd_dc)
                self.mfc_dc = None
                self._valid_dc = False

        return self

    def __exit__(self, exc_type, exc_value, traceback):
        import pywintypes
        if self.mfc_dc is not None:
            try:
                if self.mfc_dc.GetSafeHdc() != 0:
                    self.mfc_dc.DeleteDC()
            except pywintypes.error as e:
                print(f"Error deleting device context: {e}")

        if self.save_dc is not None:
            try:
                # Check if the PyCDC object is None
                if self.save_dc.GetSafeHdc() != 0:
                    self.save_dc.DeleteDC()
            except pywintypes.error as e:
                print(f"Error deleting device context: {e}")
        win32gui.ReleaseDC(HWND, self.hwnd_dc)
        if self.bitmap is not None:
            try:
                # Directly access the handle attribute of the bitmap
                handle = getattr(self.bitmap, 'GetHandle', None)
                # Check if the handle is not None and has a valid handle
                try:
                    if handle and handle() and handle() != 0:
                        win32gui.DeleteObject(handle())
                except:
                    pass
            except pywintypes.error as e:
                print(f"Error deleting bitmap: {e}")

    def is_dc_valid(self):
        return self._valid_dc

    def get_screenshot(self, region=None, dimanesion=True):
        if not self.is_dc_valid():
            return None  # Indicate failure without raising an exception
        if region:
            x, y, width, height = region['left'], region['top'], region['width'], region['height']
        windll.user32.SetProcessDPIAware()
        img = np.frombuffer(self.bmpstr, dtype=np.uint8).reshape((self.bmpinfo["bmHeight"], self.bmpinfo["bmWidth"], 4))
        img = np.ascontiguousarray(img)[..., :-1]
        img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
        if self.mfc_dc.GetSafeHdc() != 0:
            self.mfc_dc.DeleteDC()
        if self.save_dc.GetSafeHdc() != 0:
            self.save_dc.DeleteDC()
        win32gui.ReleaseDC(HWND, self.hwnd_dc)
        win32gui.DeleteObject(self.bitmap.GetHandle())
        if region:
            if dimanesion:
                full_img = img
                black_img = np.zeros_like(full_img)
                black_img[y:y+height, x:x+width] = full_img[y:y+height, x:x+width]
                return black_img
            return img[y:y+height, x:x+width]
        return img

def find_image(main_image, template):
    r_template = cv2.imread(template)
    if r_template is None:
        raise ValueError("Template image not found or unable to load.")
    if not isinstance(main_image, np.ndarray) or len(main_image.shape) != 3:
        raise ValueError("main_image must be a numpy.ndarray with 3 dimensions (height, width, channels).")
    res = cv2.matchTemplate(main_image, r_template, cv2.TM_CCOEFF_NORMED)
    threshold = 0.8
    loc = np.where(res >= threshold)
    w, h = r_template.shape[1], r_template.shape[0]
    result = None
    for pt in zip(*loc[::-1]):
        top_left = pt
        bottom_right = (pt[0] + w, pt[1] + h)
        # Calcula o centro da imagem encontrada
        center_x = pt[0] + w // 2
        center_y = pt[1] + h // 2
        result = (center_x, center_y)
        break

    if result:
        # cv2.rectangle(main_image, top_left, bottom_right, (0, 255, 0), 2)
        # cv2.imshow("Found Image", main_image)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
        return result
    return None

def look_screen(region=None, dimanesion=True):
    with WindowScreenshot() as img:
        print('Procurando imagem')
        result = img.get_screenshot(region, dimanesion)
    return result
