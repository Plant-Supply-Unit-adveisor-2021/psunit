from time import sleep
from PIL import Image, ImageDraw, ImageFont

from Adafruit_SSD1306 import SSD1306_128_64

disp = SSD1306_128_64(rst=None)

def init():
    disp = SSD1306_128_64(rst=None)
    disp.begin()
    disp.clear()
    disp.display()
    print("HEY")

def display_test():
    init()
    image = Image.new('1', (128, 64))
    draw = ImageDraw.Draw(image)
    draw.rectangle((0, 0, 128, 64), outline=0, fill=255)
    disp.image(image)
    disp.display()
    sleep(5)
    disp.clear()
    disp.display()
