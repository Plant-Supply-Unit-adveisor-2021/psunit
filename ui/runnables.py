from ui.display import FONT, S_FONT


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
    viewable to display a menu
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
        
        
class MsgViewer(Viewable):
    """
    viewable to display a string message with BACK Button
    """
    
    def __init__(self, message, back_view, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.back_view = back_view
        self.lines = []
        self.message = message
        self.split_into_lines()
        self.top = 0
                
    def split_into_lines(self):
        """
        funtion to split the text into lines
        """
        draw = self.control.oled.get_canvas()
        line = ""
        length = 0
        for word in self.message.split(' '):
            if line == "":
                # special case line empty
                nline = word
                length = draw.textsize(nline, font=S_FONT)[0]
            else:
                nline = line + " " + word
                length = draw.textsize(nline, font=S_FONT)[0]
            print(length)
            if length > 124:
                if line == "":
                    # special case line was empty -> word very long
                    self.lines.append(nline)
                    length = 0
                else:
                    self.lines.append(line)
                    line = word
                    length = draw.textsize(word, font=S_FONT)[0]
            else:
                line = nline
        self.lines.append(line)
    
    def rot_push(self):
        # go back to previous view
        self.back_view.run()
        
    def rot_clk(self):
        """"
        function called on rotary turn clkwise
        """
        # shift message down if needed
        if self.top + 4 <= len(self.lines):
            self.top += 1
        # show changes on OLED
        self.show()
        
    def rot_cclk(self):
        """
        function called on rotary turn counter clkwise
        """
        # shift message up if needed
        if self.top > 0:
            self.top -= 1
         # show changes on OLED
        self.show()
        
    def show(self):
        """
        render message view
        """
        draw = self.control.oled.get_canvas()
        # display BACK at the very top
        draw.line([0, 0, 128, 0], fill=255, width=1)
        draw.line([0, 15, 128, 15], fill=255, width=1)
        draw.text( (2, 1) , "GO BACK", font=FONT, fill=255)
        
        y = 16
        for i in range(self.top, min(len(self.lines), self.top+5)):
            draw.text( (2, y) , self.lines[i], font=S_FONT, fill=255)
            y += 10
        self.control.oled.show()
