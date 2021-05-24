from server.interface import push_data, push_images
from datetime import datetime
from time import sleep

"""

 python script to push data and images to the server

"""
# sleep to not interfere with water.py
sleep(20)
print(datetime.now().strftime("Starting push.py at %d.%m.%Y %H:%M:%S"))
push_data()
push_images()
