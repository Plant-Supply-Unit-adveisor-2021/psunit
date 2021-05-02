from signal import pause
from time import sleep

from settings import GPIO_ROT_CLK, GPIO_ROT_DT, GPIO_ROT_SW
from ui.rotary import Rotary
from ui.display import OLED
from ui.viewable import Menu

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
        
        self.view = None
        
        self.run()
    
    
    def run(self):
        """
        function to be called on userinterface startup
        """
        self.view = Menu(["Hallo", "Moin", "Einstellungen vornehmen", "BACK", "WLAN Setup", "Sonstiges"], self)
        sleep(60)
        
        
    def rot_clk(self):
        """
        function called when rotary encoder is turned clockwise
        """
        print("ROT: CLK")
        if not self.oled.alive:
            self.oled.show()
        if not self.view is None:
            self.view.rot_clk()

    def rot_cclk(self):
        """
        function called when rotary encoder is turned counter-clockwise
        """
        print("ROT: COUNTER-CLK")
        if not self.oled.alive:
            self.oled.show()
            return
        if not self.view is None:
            self.view.rot_cclk()
            
            
    def rot_push(self):
        """
        function called when rotary encoder is pushed
        """
        print("ROT: PUSH")
        if not self.oled.alive:
            self.oled.show()
            return
        if not self.view is None:
            self.view.rot_push()
