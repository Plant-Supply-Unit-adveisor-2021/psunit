import Adafruit_DHT
from settings import GPIO_DHT22


DHT_SENSOR = Adafruit_DHT.DHT22

def measure_temp_ahum():
    humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, GPIO_DHT22)

    if humidity is not None and temperature is not None:
        return (temperature, humidity)
    else:
        print("Failed to retrieve data from humidity sensor")
        return (None, None)
