from time import sleep
from threading import Timer
from PIL import Image, ImageDraw, ImageFont

from Adafruit_SSD1306 import SSD1306_128_64

from settings import OLED_TIMEOUT, OLED_SPLASH_SCREEN


def load_font(size):
    try:
        return ImageFont.truetype('DejaVuSans.ttf', size)
    except Exception:
        return ImageFont.load_default()

FONT = load_font(12)
S_FONT = load_font(10)

class OLED():
    """
    class to handle everything concerning the OLED display
    """
    
    def __init__(self):
        
        # variable to indicate if display is alive
        self.alive = False
        
        # start Display connection
        self.disp = SSD1306_128_64(rst=None)
        self.disp.begin()
        
        # initalize timer to handle timout
        self.timer = Timer(OLED_TIMEOUT, lambda : self.clear())
        self.timer.start()
        
        # initalize image to draw and show splash screen
        self.image = Image.new("1", (128, 64))
        self.splash_screen()
        
        
    def __del__(self):
        """
        clear display on program exit and shutdown timer
        """
        self.clear()
        if self.timer.is_alive():
            self.timer.cancel()
        
        
    def clear(self):
        self.disp.clear()
        self.disp.display()
        self.alive = False
    
    
    def get_canvas(self, *, empty=True):
        """
        empty: True -> new image, False -> current canvas
        returns drawing space of image
        """
        if empty:
            self.image = Image.new('1', (128, 64))
        return ImageDraw.Draw(self.image)

    
    def show(self, *, img=None):
        """
        shows self.image unless img specified
        """
        # set img to show to self.image / store img in self.image
        if img is None:
            img = self.image
        else:
            self.image = img
        # show image on screen
        self.disp.image(img)
        self.disp.display()
        self.alive = True
        
        # reset timeout
        if self.timer.is_alive():
            self.timer.cancel()
        self.timer = Timer(OLED_TIMEOUT, lambda : self.clear())
        self.timer.start()
        
        
    def splash_screen(self):
        """
        function to show a splash screen on startup
        """
        font = load_font(60)
        draw = self.get_canvas()
        draw.text((5,-2), "PSU", font=font, fill=255)
        self.show()
        sleep(OLED_SPLASH_SCREEN)
