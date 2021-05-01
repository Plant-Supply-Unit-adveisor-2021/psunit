from signal import pause
from time import sleep

from settings import GPIO_ROT_CLK, GPIO_ROT_DT, GPIO_ROT_SW
from ui.rotary import Rotary
from ui.display import OLED

class Control():
    """
    class to handle everything considering the menu and ui
    """
    
    def __init__(self):
        
        # setup rotary encoder
        self.rotary = Rotary(GPIO_ROT_CLK, GPIO_ROT_DT, GPIO_ROT_SW)
        self.rotary.set_clk(lambda : self.rot_clk())
        self.rotary.set_cclk(lambda : self.rot_cclk())
        self.rotary.set_push(lambda : self.rot_push())
        
        # setup oled display
        self.oled = OLED()
        
        self.run()
    
    
    def run(self):
        """
        function to be called on userinterface startup
        """
        draw = self.oled.get_canvas()
        draw.rectangle((0, 0, 128, 64), outline=0, fill=255)
        self.oled.show()
        sleep(3)
        draw = self.oled.get_canvas()
        draw.rectangle((0, 0, 128, 64), outline=0, fill=255)
        self.oled.show()
        sleep(90)
        
        
    def rot_clk(self):
        """
        function called when rotary encoder is turned clockwise
        """
        print("ROT: CLK")
        if not self.oled.alive:
            self.oled.show()


    def rot_cclk(self):
        """
        function called when rotary encoder is turned counter-clockwise
        """
        print("ROT: COUNTER-CLK")
        if not self.oled.alive:
            self.oled.show()
            return
            
            
    def rot_push(self):
        """
        function called when rotary encoder is pushed
        """
        print("ROT: PUSH")
        if not self.oled.alive:
            self.oled.show()
            return
