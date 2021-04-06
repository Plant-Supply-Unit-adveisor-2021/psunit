from pathlib import Path

import server.interface
from time import sleep

from datetime import datetime, timedelta
from random import random, randint
from math import log


def create_data(days, upcoming_hours, step):
    """
    function to create the data
    """
    cTime = datetime.now().replace(hour=0, minute=randint(0, 5), second=randint(0, 59),
                                   microsecond=randint(0, 999999)) - timedelta(days=days)
    print('START TIME: %s' % str(cTime))

    # starting with temperature between 5 and 20 degrees
    cTemp = random() * 15 + 5
    tempTrend = random() * 0.2 - 0.1
    # setting air humidity between 0.25 and 0.75
    cAHum = random() * 0.5 + 0.25
    # starting with ground humidity between 0 and 100
    cGHum = random()
    # starting with 70 to 100 fill level
    cFLevel = random() * 0.3 + 0.7
    # starting with brightness 0 (midnight)
    cBright = 0
    counter = 0

    while (datetime.now() - cTime) > timedelta(hours=-upcoming_hours):

        # logic for the temperature
        if cTime.hour == 3 and cTime + timedelta(minutes=step) == 4:
            tempTrend = random() * 0.2 - 0.1
        if cTime.hour < 4 or cTime.hour > 19:
            # let temperatures sink
            cTemp += (-random() * 4 + 0.5 + tempTrend) * step / 60
        elif (4 <= cTime.hour < 6) or (17 < cTime.hour <= 19):
            # let temperatures sink just a little
            cTemp += (-random() * 2 + 0.25 + tempTrend) * step / 60
        elif (6 <= cTime.hour < 8) or (15 < cTime.hour <= 17):
            # let temerature raise just a little
            cTemp += (random() * 2 - 0.25 + tempTrend) * step / 60
        else:
            # let temerature raise
            cTemp += (random() * 4 - 0.5 + tempTrend) * step / 60

        # logic for the air humidity
        cAHum = max(min(cAHum + (cTemp - 15) * 0.002 * step / 60, 1), 0)

        # logic for the brightness
        if cTime.hour < 6 or cTime.hour > 20:
            # set the brightness to 0 quickly
            cBright = max(cBright - random() * 0.3 * step / 60, 0)
        elif 6 <= cTime.hour < 9:
            # let brightness raise
            cBright = min(cBright + random() * 0.6 * step / 60, 1)
        elif 18 <= cTime.hour < 21:
            # let brightness fall
            cBright = max(cBright - random() * 0.65 * step / 60, 0)
        else:
            # hover brightness around 1 but max 1
            cBright = min(cBright + (random() * 0.25 - 0.125) * step / 60, 1)

        # logic for ground humidity and the watering of the plant
        if cTemp <= 10:
            parm = 900
        else:
            parm = 1020 - 6 * abs(cTemp) ** 1.3
        cGHum = 3.5 ** ((log(cGHum, 3.5) * parm - step) / parm)
        if random() < (cGHum + 1) ** -20:
            # watering of the plant
            cFLevel = max(cFLevel - (1 - cGHum) / 8, 0)
            cGHum = random() * 0.1 + 0.8

        # create new DataMeasurement
        server.interface.enter_data(temperature=addFail(cTemp, -10, 40, 1),
                                    air_humidity=addFail(cAHum * 100, 0, 100, 2),
                                    ground_humidity=addFail(cGHum * 100, 0, 100, 3),
                                    fill_level=addFail(cFLevel * 100, 0, 100, 1.5),
                                    brightness=addFail(cBright * 100, 0, 100, 3),
                                    timestamp=cTime)

        counter += step
        cTime = cTime + timedelta(minutes=step, seconds=randint(0, 29), microseconds=randint(0, 999999))


def addFail(value, _min, _max, failure):
    return min(_max, max(_min, value + random() * failure - failure / 2))


def test():
    #print(server.interface.register_at_server())
    # print(server.interface.post_data(23, 50, 100, 99, 20, '2021-03-28_03-03-08'))
    # server.interface.enter_data(23, 67, 100, 33, 100)
    # create_data(4, 6, 15)
    # server.interface.push_data()
    server.interface.post_image(Path('../test1.jpg'))
