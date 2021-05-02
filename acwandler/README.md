# 1. Activate the SPI bus in your Raspberry Pi
sudo raspi-config
SPI option can be found under 3. Interface Options
Activate the SPI (choose yes)
reboot the pi: sudo reboot

# 2. MCP3008.py is the class-module for the AC Wandler
example for usage can be found in the acwandler-test.py file
