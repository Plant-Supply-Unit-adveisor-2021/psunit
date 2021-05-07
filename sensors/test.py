from sensors.camera import take_picture
from sensors.pump import pump_water
from sensors.DHT22 import measure_temp_ahum
from sensors.adconverter import measure_ground_humidity, measure_light_level
from sensors.filllevel import measure_filllevel



def test():
    print("Sensors Testing ...")
    take_picture()
    pump_water(150)
    temp, humd = measure_temp_ahum()
    if not temp is None and not humd is None: 
        print("temp: {0:.2f} humid: {1:.2f}".format(temp, humd))
    print("G-Hum: {}".format(measure_ground_humidity()))
    print("Light: {}".format(measure_light_level()))
    # print(measure_filllevel())
