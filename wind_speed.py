from gpiozero import Button

import time
import datetime

import math
import statistics

# adjust for anemometer factor
# resulting from the wind energy lost when the arms turn
ADJUSTMENT = 1.18
CM_IN_KM = 100000.00
SEC_IN_HOUR = 3600

wind_count = 0
radius_cm = 9.0 # radius of anemometer
wind_interval = 5 # how often to report speed

# wind speed readings list
store_speeds = []

# every half rotation, add 1 to count
def spin():
    global wind_count
    wind_count = wind_count + 1
    
# calculate the wind speed
def calculate_speed(time_sec):
    global wind_count
    
    circumference_cm = (2 * math.pi) * radius_cm
    rotations = wind_count / 2.0

    # calculate distance travelled by a cup in cm
    dist_cm = circumference_cm * rotations
    dist_km = dist_cm/CM_IN_KM # convert cm to km

    # convert seconds to hours
    km_per_sec = dist_km / time_sec
    km_per_hour = km_per_sec * SEC_IN_HOUR
    
    return km_per_hour * ADJUSTMENT

def reset_wind():
    global wind_count
    wind_count = 0

EPOCH = datetime.datetime.utcfromtimestamp(0)
def currentEpoch():
    return int((datetime.datetime.now() - EPOCH).total_seconds() * 1000)

wind_speed_sensor = Button(5)
wind_speed_sensor.when_pressed = spin

# loop to measure wind speed
# report at 5 second intervals
while True:
    start_time = time.time()
    while time.time() - start_time <= wind_interval:
        reset_wind()
        
        time.sleep(wind_interval)
        speed = calculate_speed(wind_interval)
        store_speeds.append(speed)

    max_speed = max(store_speeds) # wind gust
    last_speed = store_speeds[-1]
    avg_speed = statistics.mean(store_speeds)
    print(currentEpoch(), avg_speed, max_speed, last_speed)
