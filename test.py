from time import sleep

from server.test import test as server_test
from sensors.test import test as sensors_test
from ui.test import test as ui_test

from settings import MEASURE_CONFIG

if MEASURE_CONFIG['DHT22']:
    print('YEAH')
else:
    print('SAD')

#while(True):
#    sensors_test()
#    sleep(5)
# server_test()
# ui_test()
