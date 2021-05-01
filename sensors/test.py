from signal import pause

from sensors import ROTARY
from sensors.camera import make_picture
from sensors.pump import pump_water
from sensors.display import display_test

def test():
    print("Sensors Testing ...")
    # take_picture()
    # pump_water(150)
    # display_test()
    ROTARY.set_clk(lambda : print("clk"))
    ROTARY.set_cclk(lambda : print("cclk"))
    ROTARY.set_push(lambda : print("push"))
    pause()
