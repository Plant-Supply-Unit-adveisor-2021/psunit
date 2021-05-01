from gpiozero import DigitalOutputDevice
from time import sleep

from settings import GPIO_PUMP

SECONDS_PER_MILLILITER = 0.0616

def pump_water(amount):
    """
    function to pump water
    amount in milliliters
    """
    print(amount * SECONDS_PER_MILLILITER)
    pump = DigitalOutputDevice(GPIO_PUMP)
    pump.on()
    sleep(amount * SECONDS_PER_MILLILITER)
    pump.off()
