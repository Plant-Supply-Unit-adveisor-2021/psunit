import os
from datetime import datetime

DATA_DIR = '../psunit_data/'

def enter_measurement(temperature, air_humidity, ground_humidity, brightness, fill_level, *, timestamp=datetime.now()):
    """
    function used to enter the measured data
    the data will be stored in the data directory to keep it stored locally for backup purposes
    additionally these files will be used to post the data
    """

    # create data directory
    os.makedirs(DATA_DIR + 'measurements/', exist_ok=True)

    # write data entry
    file = open(DATA_DIR + 'measurements/' + timestamp.strftime('%Y-%m-%d') + '.log', 'a')
    file.write(timestamp.strftime('%Y-%m-%d_%H-%M-%S') + ';' +
               str(temperature) + ';' + str(air_humidity) + ';' + str(ground_humidity) + ';' +
               str(brightness) + ';' + str(fill_level) + '\n')
    file.close()


def enter_image(image):
    """
    function used to enter a image
    the image will be stored locally for backup purposes
    these local files wll be used by the server.interface to push the image
    image: PIL/Pillow image object
    """
    
    # create data directory
    os.makedirs(DATA_DIR + 'images/', exist_ok=True)
    
    image.save(DATA_DIR + 'images/test.jpeg')
