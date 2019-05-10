from gpiozero import MCP3008

import time
import datetime

import math

adc = MCP3008(channel=0)

volts = { 
    0.1 : 270.0, 
    0.2 : 315.0, 
    0.3 : 292.5, 
    0.4 : 0.0, 
    0.6 : 337.5, 
    0.7 : 225.0, 
    0.8 : 247.5, 
    1.2 : 45.0, 
    1.4 : 22.5, 
    1.8 : 180.0, 
    2.0 : 202.5, 
    2.2 : 135.0, 
    2.5 : 157.5, 
    2.7 : 90.0, 
    2.8 : 67.5, 
    2.9 : 112.5
}

EPOCH = datetime.datetime.utcfromtimestamp(0)
def currentEpoch():
    return int((datetime.datetime.now() - EPOCH).total_seconds() * 1000)


# directional statistics
# https://en.wikipedia.org/wiki/Directional_statistics
def get_average(angles):
    
    average = -1.0

    sin_sum = 0.0
    cos_sum = 0.0

    for angle in angles:
        r = math.radians(angle)
        sin_sum += math.sin(r)
        cos_sum += math.cos(r)
    
    flen = float(len(angles))
    if flen == 0:
        print(
            "ERROR: len(angles) == 0 (angles: {}, sin_sum: {}, cos_sum: {}".format(
                angles, sin_sum, cos_sum
            )
        )
    else:
        s = sin_sum /flen
        c = cos_sum /flen

        arc = math.degrees(math.atan(s / c))    

        if s > 0 and c > 0:
            average = arc
        elif c < 0:
            average = arc + 180
        elif s < 0 and c > 0:
            average = arc + 360

    return 0.0 if average == 360 else average

def get_value(interval=5):
    data = []
    start_time = time.time()

    while time.time() - start_time < interval:
        wind = round(adc.value * 3.3, 1)
        if wind in volts:
            data.append(volts[wind])
        #else:
        #    print('unknown value: ' + str(wind)) 

        #if not wind in volts: # keep only good measurements
        #    print('unknown value: ' + str(wind)) 
        #else:
        #    data.append(volts[wind])

    return get_average(data)

#while True:
#    print(currentEpoch(), get_value())

'''
while True:
    wind = round(adc.value * 3.3, 1)
    if not wind in volts:
        print('unknown value: ' + str(wind) + ' ' + str(volts[wind]))   
    else:
        print('match: ' + str(wind) + ' ' + str(volts[wind]))
'''