from sensors.hx711 import HX711
import RPi.GPIO as GPIO

# Initialisierung
REFERENCE_UNIT = -43
TANK_MIN = -4133
TANK_MAX = -3510

def measure_filllevel():
    """
    function to measure the filllevel
    """
    
    hx = HX711(5, 6) #(DT_out, pd_sck)
    hx.set_reading_format("MSB", "MSB")
    hx.set_reference_unit(REFERENCE_UNIT)
    hx.reset()

    # Sensoren auslesen
    val = hx.get_weight(5)

    # Füllstandswertrückgabe
    if val < TANK_MIN:
        return 0
    
    if val > TANK_MAX:
        return 100
    
    else:
        vol = TANK_MAX - TANK_MIN 
        füllstand = val - TANK_MIN
        return (füllstand / vol) * 100

    hx.power_down()
    #hx.power_up()
    GPIO.cleanup()

def cleanAndExit():
    GPIO.cleanup()

def tare():
    hx.tare()


def setup():
    if referenceUnit == 1: 
        print("Tare...")
        #tare()
        
    
    while True:
        try:
            val = sum(hx.get_raw_data(100))/100
            print(val)
            hx.power_down()
            hx.power_up()
            time.sleep(0.1)
        
        except (KeyboardInterrupt, SystemExit):
            cleanAndExit()


"""
while True:
    try:
        tank = füllstand()
        print("Tankfüllung: %.2f %%" % (tank * 100)) 
    
    except (KeyboardInterrupt, SystemExit):
        cleanAndExit()
"""