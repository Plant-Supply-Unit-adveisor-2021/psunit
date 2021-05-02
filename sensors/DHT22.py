import Adafruit_DHT

DHT_SENSOR = Adafruit_DHT.DHT22
DHT_PIN = 4

def measure_temp_ahum():
    humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)

    if humidity is not None and temperature is not None:
        return (temperature, humidity)
    else:
        print("Failed to retrieve data from humidity sensor")
        return (None, None)
