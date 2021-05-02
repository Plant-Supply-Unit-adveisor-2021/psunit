from pathlib import Path
import os

"""

    This file is used to hold constansts

"""

# Pump
GPIO_PUMP = 21

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
