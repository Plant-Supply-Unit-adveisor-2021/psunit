from spidev import SpiDev
 
  # define the wandler-class
class MCP3008:
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
adc = MCP3008()

# funktion für das Auslesen der rohen Daten der sensoren
def rawValue(n): # n = Nummer des auszulesenden Channel
    return adc.read(channel = n)

# bodenfeucht

# grenzwerte
AirValue = 616
WaterValue = 335

def getBodenfeucht(n): #n ist die Nummer der Channel, an der der Sensor angeschlossen ist
    raw = rawValue(n)
    value_in_procent = 1 - ((raw - WaterValue)/(AirValue - WaterValue))
    if value_in_procent < 0:
       value_in_procent = 0
    elif value_in_procent > 1:
       value_in_procent = 1
    return 100 * value_in_procent #angabe in prozent
 
#Fotowiederstand
def getLight(n):
    MaxWert = 1023
    Light = rawValue(n)
    value = 4000 * (1 - (x / 1023)) #angabe in absoluten Werten
    return value
