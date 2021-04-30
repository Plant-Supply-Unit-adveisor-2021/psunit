from sensors.rotary import Rotary

"""
configuration of pins and co
"""

GPIO_PUMP = 21
ROTARY = Rotary(pin_clk=27, pin_dt=22, pin_sw=17)
