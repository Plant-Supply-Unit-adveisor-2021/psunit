# psunit
Software for the Plant Supply Units

# Installation process
First of all you have to enable the camera, I²C and SPI in the configuration of the Raspberry Pi (`sudo raspi-config` -> interfaces).
Afterwards you should reboot your pi.

Going on you should clone this repository and run the following command inside the repository.

    pip3 install -r requirements.txt

Afterwards you should configure your crontab file to call the measure.py and the push.py on a regualar bases. In order to function properly the psuserver needs to be running on the other side.

# credits 
Thanks to @tatobari whos hx711 libary we are using. https://github.com/tatobari/hx711py