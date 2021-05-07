from gpiozero import DigitalOutputDevice
from time import sleep

from settings import MEASURE_CONFIG, GPIO_PUMP

SECONDS_PER_MILLILITER = 0.0616

def pump_water(amount):
    """
    function to pump water
    amount in milliliters
    """
    if not MEASURE_CONFIG['PUMP']:
        # pump not activated in settings
        print('PUMP not activated in measure.config.json')
        return
    
    print('PUMP: Watering plant with {}ml of water.'.format(amount))
    pump = DigitalOutputDevice(GPIO_PUMP)
    pump.on()
    sleep(amount * SECONDS_PER_MILLILITER)
    pump.off()
    pump.close()
