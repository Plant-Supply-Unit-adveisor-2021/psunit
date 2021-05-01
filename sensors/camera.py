from picamera import PiCamera
from time import sleep
from io import BytesIO
from PIL import Image

from server.enter_data import enter_image

def take_picture():
    """
    function to take a photo and store it to be pushed to the server
    """
    
    # setup camera and stream
    stream = BytesIO()
    camera = PiCamera()
    camera.resolution = (1280, 720)
    camera.start_preview(alpha=200)
    # sleep for 3 secs to let the camera adopt to environment
    sleep(3)
    
    # capture photo to stream
    camera.capture(stream, format='jpeg')
    camera.stop_preview()
    
    # rewind stream and convert it to PIL image
    stream.seek(0)
    image = Image.open(stream)
    
    # hand over image to the handling of storing/pushing
    enter_image(image)
