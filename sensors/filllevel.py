from sensors.hx711 import HX711
from settings import MEASURE_CONFIG, save_measure_config
import RPi.GPIO as GPIO
from traceback import format_exc

# Initalisation
REFERENCE_UNIT = -43

def measure_filllevel():
    """
    function to measure the filllevel
    """
    
    if not MEASURE_CONFIG['HX711']:
        print("HX711 not activated in measure.config.json")
        return None
    
    try:
        # remove bloody warnings
        # GPIO.setwarnings(False)
        # GPIO.setmode(GPIO.BCM)
        
        hx = HX711(MEASURE_CONFIG['GPIO_HX711_DT'], MEASURE_CONFIG['GPIO_HX711_SCK']) #(DT_out, pd_sck)
        hx.set_reading_format("MSB", "MSB")
        hx.set_reference_unit(REFERENCE_UNIT)
        hx.reset()

        # read sensor data
        val = hx.get_weight(25)
        hx.power_down()
        # GPIO.cleanup()
        # print(val)

        # calculate result and return it
        percentage = (val - MEASURE_CONFIG['HX711_MINV'])/(MEASURE_CONFIG['HX711_MAXV'] - MEASURE_CONFIG['HX711_MINV'])
        return 100 * max(0, min(1, percentage))
        
    except Exception:
        print(format_exc())
        return None
        
        
def set_extreme_value(full):
    """
    function used to set the extreme values of the filllevel
    full: True -> set max value, False -> set min value
    returns: True if everything worked out as expected
    """
    if not MEASURE_CONFIG['HX711']:
        print("HX711 not activated in measure.config.json")
        return False
    
    try:
        # remove bloody warnings
        # GPIO.setwarnings(False)
        # GPIO.setmode(GPIO.BCM)
        
        hx = HX711(MEASURE_CONFIG['GPIO_HX711_DT'], MEASURE_CONFIG['GPIO_HX711_SCK']) #(DT_out, pd_sck)
        hx.set_reading_format("MSB", "MSB")
        hx.set_reference_unit(REFERENCE_UNIT)
        
        val = 0
        # read sensor data
        for i in range(0, 5):
            hx.reset()
            val += hx.get_weight(101)/5
        hx.power_down()
        # GPIO.cleanup()
        print(val)

        # set new extreme
        if not full:
            MEASURE_CONFIG['HX711_MINV'] = val
        else:
            MEASURE_CONFIG['HX711_MAXV'] = val
        save_measure_config()
        return True
        
    except Exception:
        print(format_exc())
        return False
