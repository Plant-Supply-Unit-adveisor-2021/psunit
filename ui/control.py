from signal import pause
from time import sleep

from settings import GPIO_ROT_CLK, GPIO_ROT_DT, GPIO_ROT_SW
from ui.rotary import Rotary
from ui.display import OLED

def initalize():
    """
    function to be called on userinterface startup
    """
    rotary = Rotary(GPIO_ROT_CLK, GPIO_ROT_DT, GPIO_ROT_SW)
    rotary.set_clk(lambda : print("clk"))
    rotary.set_cclk(lambda : print("cclk"))
    rotary.set_push(lambda : print("push"))
    
    oled = OLED()
    oled.display_test()
    sleep(90)

def control_test():
    rotary = Rotary(GPIO_ROT_CLK, GPIO_ROT_DT, GPIO_ROT_SW)
    rotary.set_clk(lambda : print("clk"))
    rotary.set_cclk(lambda : print("cclk"))
    rotary.set_push(lambda : print("push"))
    pause()
