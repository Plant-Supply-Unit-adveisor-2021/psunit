from picamera import PiCamera
from time import sleep
from datetime import datetime

def make_picture():
    print("Starting Camera Setup ...")
    camera = PiCamera()
    camera.resolution = (1280, 720)
    camera.start_preview(alpha=200)
    sleep(2)
    print("Picture in 1 sec")
    sleep(1)
    camera.capture('../test.jpg')
    camera.stop_preview()
