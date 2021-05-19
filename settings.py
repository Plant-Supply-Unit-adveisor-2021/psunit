from pathlib import Path
import os
from json import dump as json_dump, load as json_load

"""

    This file is used to hold constants and the current measure config

"""

# OLED variables in seconds
# connect to I2C interface

# Setup of the data directory
DATA_DIR = os.path.join(Path(__file__).parent.parent.absolute(), 'psunit_data')
MEASUREMENT_DIR = os.path.join(DATA_DIR, 'measurements')
IMAGE_DIR = os.path.join(DATA_DIR, 'images')
UI_LOG_DIR = os.path.join(DATA_DIR, 'ui_log')

# configuration of the measure config
# the measure config holds all settings which might be changed individually
MC_FILE = os.path.join(DATA_DIR, "measure.config.json")
MEASURE_CONFIG = {
    # DHT22
    'DHT22': True,
    'GPIO_DHT22': 25,
    # AD-Converter
    # connect ADC to SPI of Raspberry and CE0
    # channels of analog sources (ground humidity and ldr)
    'CH_GHUM': 6,
    'CH_LIGHT': 7,
    'G_HUM': True,
    'G_HUM_MINV': 900, # value of ADC to be considered 0% humidity
    'G_HUM_MAXV': 450, # value of ADC to be considered 100% humidity
    'LDR': True,
    'LDR_MINV': 42,  # value of ADC to be considered 0% light
    'LDR_MAXV': 920, # value of ADC to be considered 100% light
    # HX711
    'HX711': True,
    'GPIO_HX711_DT': 26,
    'GPIO_HX711_SCK': 19,
    'HX711_MINV': -4133,
    'HX711_MAXV': -3510,
    # Pump
    'PUMP': True,
    'GPIO_PUMP': 21,
    # Rotary Encoder
    'ROTARY_ENC': True,
    'GPIO_ROT_CLK': 27,
    'GPIO_ROT_DT': 22,
    'GPIO_ROT_SW': 17,
    # OLED Display at I2C of Raspi
    'OLED': True,
    'OLED_TIMEOUT': 5,
    'OLED_SPLASH_SCREEN': 1,
    # Camera at camera connector
    'CAMERA': True,
}

if os.path.exists(MC_FILE):
    # load measure config
    MEASURE_CONFIG = json_load(open(MC_FILE, 'r'))
else:
    # create measure config and initialize it
    os.makedirs(DATA_DIR, exist_ok=True)
    os.mknod(MC_FILE)
    json_dump(MEASURE_CONFIG, open(MC_FILE, 'w'))
    

def save_measure_config():
    """
    function to save the current MEASUER_CONFIG dict to the corresponding file
    """
    json_dump(MEASURE_CONFIG, open(MC_FILE, 'w'))
