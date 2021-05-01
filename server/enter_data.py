import os
from datetime import datetime

from settings import DATA_DIR, MEASUREMENT_DIR, IMAGE_DIR


def enter_measurement(temperature, air_humidity, ground_humidity, brightness, fill_level, *, timestamp=datetime.now()):
    """
    function used to enter the measured data
    the data will be stored in the data directory to keep it stored locally for backup purposes
    additionally these files will be used to post the data
    """

    # create data directory
    os.makedirs(MEASUREMENT_DIR, exist_ok=True)

    # write data entry
    file = open(os.path.join(MEASUREMENT_DIR, timestamp.strftime('%Y-%m-%d') + '.log'), 'a')
    file.write(timestamp.strftime('%Y-%m-%d_%H-%M-%S') + ';' +
               str(temperature) + ';' + str(air_humidity) + ';' + str(ground_humidity) + ';' +
               str(brightness) + ';' + str(fill_level) + '\n')
    file.close()


def enter_image(image, *, timestamp=datetime.now()):
    """
    function used to enter a image
    the image will be stored locally for backup purposes
    these local files wll be used by the server.interface to push the image
    image: PIL/Pillow image object
    timestamp: timestamp of the picture for the database
    """
    
    # create data directory
    imgdir = os.path.join(IMAGE_DIR,timestamp.strftime('%Y-%m-%d'))
    os.makedirs(imgdir, exist_ok=True)
    
    # add special image processing here if needed (e.g. timestamp text)
    
    image.save(os.path.join(imgdir, timestamp.strftime('%Y-%m-%d_%H-%M-%S') + '.jpeg'))
