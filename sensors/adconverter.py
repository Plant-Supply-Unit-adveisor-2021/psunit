from spidev import SpiDev
from time import sleep

from settings import MEASURE_CONFIG, CH_GHUM, CH_LIGHT
 
class MCP3008:
    """
    class to control the analog-digital-converter
    """
    def __init__(self, bus = 0, device = 0):
        self.bus, self.device = bus, device
        self.spi = SpiDev()
        self.open()
        self.spi.max_speed_hz = 1000000 # 1MHz
 
    def open(self):
        self.spi.open(self.bus, self.device)
        self.spi.max_speed_hz = 1000000 # 1MHz
    
    def read(self, channel = 0):
        adc = self.spi.xfer2([1, (8 + channel) << 4, 0])
        data = ((adc[1] & 3) << 8) + adc[2]
        return data
            
    def close(self):
        self.spi.close()


def measure_ground_humidity():
    """
    returns: ground humidity in percent (0 - 100) or None if there is an error
    """
    try:
        if not MEASURE_CONFIG['G_HUM']:
            # G_HUM not enabled in measure.config.json
            print('G_HUM not activated in measure.config.json')
            return None
        
        # initiate the ac wandler
        ADC = MCP3008()
        
        # make 5 measurements and take arithmetric middle
        raw = 0
        for i in range(0, 5):
            raw += ADC.read(CH_GHUM)/5
            sleep(0.1)
            
        # close ADC interface
        ADC.close()
        
        # calculate result and return it
        percentage = abs((raw - MEASURE_CONFIG['G_HUM_MINV'])/(MEASURE_CONFIG['G_HUM_MINV'] - MEASURE_CONFIG['G_HUM_MAXV']))
        return 100 * max(0, min(1, percentage))
    except Exception as e:
        print('MCP3008 could not measure grund humidity due to an exception')
        print(e)
    try:
        # Try to close ADC
        ADC.close()
    except:
        pass
    return None


def measure_light_level():
    """
    returns: light level in percent (0 - 100)  or None if there is an error
    """
    # make 5 measurements and take arithmetric middle
    try:
        if not MEASURE_CONFIG['LDR']:
            # LDR not enabled in measure.config.json
            print('LDR not activated in measure.config.json')
            return None
        
        # initiate the ac wandler
        ADC = MCP3008()
        
        # make 5 measurements and take arithmetric middle
        raw = 0
        for i in range(0, 5):
            raw += ADC.read(CH_LIGHT)/5
            sleep(0.1)
            
        # close ADC interface
        ADC.close()
        
        # calculate result and return it
        percentage = abs((raw - MEASURE_CONFIG['LDR_MINV'])/(MEASURE_CONFIG['LDR_MINV'] - MEASURE_CONFIG['LDR_MAXV']))
        return 100 * max(0, min(1, percentage))
    except Exception as e:
        print('MCP3008 could not measure light level due to an exception')
        print(e)
    try:
        # Try to close ADC
        ADC.close()
    except:
        pass
    return None
