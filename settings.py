from pathlib import Path
import os
from json import dump as json_dump, load as json_load

"""

    This file is used to hold constants and the current measure config

"""

# Pump
GPIO_PUMP = 21

# DHT22
GPIO_DHT22 = 25

# AD-Converter
# connect ADC to SPI of Raspberry and CE0
# channels of analog sources
CH_GHUM = 6
CH_LIGHT = 7

# Rotary Encoder
GPIO_ROT_CLK = 27
GPIO_ROT_DT = 22
GPIO_ROT_SW = 17

# OLED variables in seconds
OLED_TIMEOUT = 5
OLED_SPLASH_SCREEN = 1

# Setup of the data directory
DATA_DIR = os.path.join(Path(__file__).parent.parent.absolute(), 'psunit_data')
MEASUREMENT_DIR = os.path.join(DATA_DIR, 'measurements')
IMAGE_DIR = os.path.join(DATA_DIR, 'images')
UI_LOG_DIR = os.path.join(DATA_DIR, 'ui_log')

# configuration of the measure config
MC_FILE = os.path.join(DATA_DIR, "measure.config.json")
MEASURE_CONFIG = {
    'DHT22': True,
    'HX711': True,
    'G_HUM': True,
    'LDR': True,
    'PUMP': True,
    'ROTOARY_ENC': True,
    'OLED': True,
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
