from sensors.camera import make_picture
from sensors.pump import pump_water
from sensors.DHT22 import measure_temp_ahum  


def test():
    temp, humd = measure_temp_ahum()
    print("temp: {0:.2f} humid: {1:.2f}".format(temp, humd))
    print("Sensors Test")
    # pump_water(150)
