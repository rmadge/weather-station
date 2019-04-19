
from gpiozero import Button

import time
import datetime

rain_sensor = Button(6)
BUCKET_SIZE = 0.2794
count = 0

def bucket_tipped():
    global count
    count += 1
    print(count * BUCKET_SIZE)

def reset_rainfall():
    global count
    count = 0

rain_sensor.when_pressed = bucket_tipped

EPOCH = datetime.datetime.utcfromtimestamp(0)
def currentEpoch():
    return int((datetime.datetime.now() - EPOCH).total_seconds() * 1000)

while True:
    time.sleep(1)