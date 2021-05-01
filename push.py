from server.interface import push_data, push_images
from datetime import datetime

"""

 python script to push data and images to the server

"""

print(datetime.now().strftime("Starting push.py at %d.%m.%Y %H:%M:%S"))
push_data()
push_images()
