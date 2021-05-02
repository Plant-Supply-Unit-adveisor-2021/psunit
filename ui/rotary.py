from gpiozero import Button, RotaryEncoder

class Rotary:
    """
    class to control the rotary encoder and assign event funcions
    """
    
    def __init__(self, pin_clk, pin_dt, pin_sw):
        """
        pin_clk: GPIO number of clk pin
        pin_dt: GPIO number of dt pin
        pin_sw GPIO number of sw pin
        """
        self.rotary = RotaryEncoder(pin_clk, pin_dt)
        self.button = Button(pin_sw)
        
    def set_clk(self, function):
        """
        function to set the function to be executed on clockwise turn
        """
        self.rotary.when_rotated_clockwise = function
        
    def set_cclk(self, function):
        """
        function to set the function to be executed on counter clockwise turn
        """
        self.rotary.when_rotated_counter_clockwise = function
        
    def set_push(self, function):
        """
        function to set the function to be executed on button press
        """
        self.button.when_pressed = function
