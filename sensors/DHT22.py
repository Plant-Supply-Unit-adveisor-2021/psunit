from Adafruit_DHT import DHT22, read_retry
from settings import MEASURE_CONFIG, GPIO_DHT22

def measure_temp_ahum():
    """
    function with measures temperature and air humidity via the DHT22
    returns: tuple (temp, a_hum) and (None, None) if something failed
    """
    try:
        if not MEASURE_CONFIG['DHT22']:
            # DHT22 not enabled in measure.config.json
            print('DHT22 not activated in measure.config.json')
            return (None, None)
    
        humidity, temperature = read_retry(DHT22, GPIO_DHT22)

        if humidity is not None and temperature is not None:
            return (temperature, humidity)
        else:
            print("DHT22: Failed to retrieve data from temp and humidity sensor")
            return (None, None)
    except Exception as e:
        print("DHT22: Failed to retrieve data from temp and humidity sensor due to error")
        print(e)
        return (None, None)
