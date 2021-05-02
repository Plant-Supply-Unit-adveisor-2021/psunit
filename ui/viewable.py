from ui.display import FONT

class Viewable:
    """
    parent class to hold a viewable
    """
    
    def __init__(self, control):
        # holds object of ui.control.Control to handle in/out
        self.control = control

    def rot_clk(self):
        # function called on rotary turn clkwise
        pass
        
    def rot_cclk(self):
        # function called on rotary turn counter clkwise
        pass
        
    def rot_push(self):
        # function called on rotary push
        pass
        
    def show(self):
        # function to start showing the view
        pass
        

class Menu(Viewable):
    """
    class which holds all the necessary data for a menu
    """
    
    def __init__(self, entries, *args, **kwargs):
        """
        entries: list of strings for now
        """
        super().__init__(*args, **kwargs)
        
        self.entries = entries
        # current selected entry
        self.active = 0
        # variable to hold begin of the viewable list (max 4 entries)
        self.top = 0
        
        self.show()
        
    def rot_clk(self):
        """"
        function called on rotary turn clkwise
        """
        print("MENU CLK")
        # set new active element
        if self.active < len(self.entries) - 1:
            self.active += 1
        # shift list down if needed
        if self.active >= self.top+3 and self.top+3 <= len(self.entries):
            self.top += 1
        # show changes on OLED
        self.show()
        
    def rot_cclk(self):
        """
        function called on rotary turn counter clkwise
        """
        print("MENU CCLK")
        # set new active element
        if self.active > 0:
            self.active -= 1
        # shift list up if needed
        if self.active <= self.top and self.top > 0:
             self.top -= 1
         # show changes on OLED
        self.show()
        
    def rot_push(self):
        # function called on rotary push
        print("MENU PUSH")
        
    def show(self):
        """
        renders the menu and shows it on OLED
        """
        draw = self.control.oled.get_canvas()
        count = 0
        for i in range(self.top, min(self.top+4, len(self.entries))):
            if i == self.active:
                y = 16*count
                draw.line([0, y, 128, y], fill=255, width=1)
                draw.line([0, y+15, 128, y+15], fill=255, width=1)
            draw.text( (2, 16*count + 1) , self.entries[i], font=FONT, fill=255)
            count += 1
        self.control.oled.show()

