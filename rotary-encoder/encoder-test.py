from RPi import GPIO
from time import sleep

# pins setup
clk = 17
dt = 18
sw = 27

# gpio setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(clk, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(dt, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(sw, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

#initial states
counter = 0
pushed = False #for the button
clkLastState = GPIO.input(clk)
swLastState = GPIO.input(sw)


try:

        while True:
                # drehen
                clkState = GPIO.input(clk)
                dtState = GPIO.input(dt)
                if clkState != clkLastState:
                        if dtState != clkState:
                                counter += 1
                        else:
                                counter -= 1
                        print (counter)
                clkLastState = clkState
                
                # druecken
                swState = GPIO.input(sw)
                if swState != swLastState:
                 pushed = not pushed
                 print(pushed)
                 swLastState  = swState
                 
                sleep(0.01)
finally:
        GPIO.cleanup()
