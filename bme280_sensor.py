import bme280
import smbus2

import time
import datetime

port = 1
address = 0x77
bus = smbus2.SMBus(port)

bme280.load_calibration_params(bus, address)

def read_all():
    bme280_data = bme280.sample(bus, address)
    return bme280_data.humidity, bme280_data.pressure, bme280_data.temperature

EPOCH = datetime.datetime.utcfromtimestamp(0)
def currentEpoch():
    return int((datetime.datetime.now() - EPOCH).total_seconds() * 1000)

#while True:
    #print(read_all())
    #time.sleep(1)
