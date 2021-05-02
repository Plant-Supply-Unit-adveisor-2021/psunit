from ui.display import FONT

class Runnable:
    """
    parent class to run some action, e.g. show viewable, ...
    """
    def __init__(self, control):
        # holds object of ui.control.Control to handle in/out
        self.control = control

    def run(self):
        # entrypoint of runnable
        pass


class Viewable(Runnable):
    """
    parent class to hold a viewable
    """

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
        
    def run(self):
        # entrypoint of viewable
        self.control.set_view(self)
        self.show()
        

class Menu(Viewable):
    """
    class which holds all the necessary data for a menu
    """
    
    def __init__(self, entries, runnables, *args, **kwargs):
        """
        entries: list of strings
        viewables: list of corresponding views to enter on push
        """
        super().__init__(*args, **kwargs)
        
        self.entries = entries
        self.runnables = runnables
        # current selected entry
        self.active = 0
        # variable to hold begin of the viewable list (max 4 entries)
        self.top = 0
        
    def rot_clk(self):
        """"
        function called on rotary turn clkwise
        """
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
        if (self.active < len(self.runnables) and
           not self.runnables[self.active] is None):
            self.runnables[self.active].run()

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

