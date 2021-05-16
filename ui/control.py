from signal import pause
from time import sleep

from settings import MEASURE_CONFIG
from ui.rotary import Rotary
from ui.display import OLED
from ui.menus import MenuTree

class Control():
    """
    class to handle everything considering the menu and ui
    """
    
    def __init__(self):
        
        # setup rotary encoder
        self.rotary = Rotary(MEASURE_CONFIG['GPIO_ROT_CLK'],
                             MEASURE_CONFIG['GPIO_ROT_DT'],
                             MEASURE_CONFIG['GPIO_ROT_SW'])
        self.rotary.set_clk(lambda : self.rot_clk())
        self.rotary.set_cclk(lambda : self.rot_cclk())
        self.rotary.set_push(lambda : self.rot_push())
        
        # setup oled display
        self.oled = OLED()
        
        self.view = None
        self.menu_tree = MenuTree(self)
        self.run()
    
    def run(self):
        """
        function to be called on userinterface startup
        """
        # run as long as not terminated
        pause()
        
    def set_view(self, view):
        """
        called bzy viewables to connect to input
        """
        self.view = view
        
        
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
