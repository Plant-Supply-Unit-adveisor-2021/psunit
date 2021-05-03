from datetime import datetime

from sensors.DHT22 import measure_temp_ahum
from sensors.adconverter import measure_ground_humidity, measure_light_level
from sensors.camera import take_picture
from server.enter_data import enter_measurement
from sensors.filllevel import measure_filllevel

# this script needs to be called by a cron job to take measurements

print(datetime.now().strftime("Starting measure.py at %d.%m.%Y %H:%M:%S"))
ghum = measure_ground_humidity()
light = measure_light_level()
temp, ahum = measure_temp_ahum()
fill = measure_filllevel()
enter_measurement(temp, ahum, ghum, light, fill)
take_picture()
