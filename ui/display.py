from time import sleep
from threading import Timer
from PIL import Image, ImageDraw, ImageFont

from Adafruit_SSD1306 import SSD1306_128_64

from settings import OLED_TIMEOUT


class OLED():
    """
    class to handle everything concerning the OLED display
    """
    
    def __init__(self):
        
        # Start Display connection
        self.disp = SSD1306_128_64(rst=None)
        # Initalize screensize
        self.disp.begin()
        self.clear()
        # initalize image to draw
        self.image = Image.new("1", (128, 64))
        
        # initalize timer to handle timout
        self.timer = Timer(OLED_TIMEOUT, lambda : self.clear())
        self.timer.start()
        
        
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
        
        # reset timeout
        if self.timer.is_alive():
            self.timer.cancel()
        self.timer = Timer(OLED_TIMEOUT, lambda : self.clear())
        self.timer.start()
    
    
    def display_test(self):
        draw = self.get_canvas()
        draw.rectangle((0, 0, 128, 64), outline=0, fill=255)
        self.show()
