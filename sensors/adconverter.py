from spidev import SpiDev
from time import sleep

from settings import CH_GHUM, CH_LIGHT
 
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


# initiate the ac wandler
ADC = MCP3008()


# ground humidity
# extreme values of ground humdity read-out
GHUM_AIR = 900
GHUM_WATER = 380

def measure_ground_humidity():
    """
    returns: ground humidity in percent (0 - 100)
    """
    # make 5 measurements and take arithmetric middle
    raw = 0
    for i in range(0, 5):
        raw += ADC.read(CH_GHUM)/5
        sleep(0.1)
    print(raw)
    percentage = 1 - (raw - GHUM_WATER)/(GHUM_AIR - GHUM_WATER)
    return 100 * max(0, min(1, percentage))
 

# light sensor (LDR)
# extreme values of light read-out
LIGHT_MAX = 920
LIGHT_MIN = 45

def measure_light_level():
    """
    returns: light level in percent (0 - 100)
    """
    # make 5 measurements and take arithmetric middle
    raw = 0
    for i in range(0, 5):
        raw += ADC.read(CH_LIGHT)/5
        sleep(0.1)
    print(raw)
    percentage = (raw - LIGHT_MIN)/(LIGHT_MAX - LIGHT_MIN)
    return 100 * max(0, min(1, percentage))
 
