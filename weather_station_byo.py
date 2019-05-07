from gpiozero import Button

import time
import datetime
import json

import math
import statistics

import wind_direction_byo
import ds18b20_therm
import bme280_sensor

from kafka import KafkaProducer
from kafka.errors import KafkaError

def publish(msg):
    brokers = 
    topic = 'weather-station'
    producer = KafkaProducer(bootstrap_servers=brokers)
    future = producer.send(topic, str.encode(msg))
    try:
        record_metadata = future.get(timeout=10)
    except KafkaError as ke:
        print(ke)
        pass

# adjust for anemometer factor
# resulting from the wind energy lost when the arms turn
ADJUSTMENT = 1.18
CM_IN_KM = 100000.00
SEC_IN_HOUR = 3600

wind_count = 0
radius_cm = 9.0 # radius of anemometer

interval = 30  # reading interval
wind_interval = 5 # how often to report speed

# wind speed readings list
store_speeds = []
store_directions = []

# rainfall
BUCKET_SIZE = 0.2794
rain_count = 0

def bucket_tipped():
    global rain_count
    rain_count += 1
    #print(count * BUCKET_SIZE)

def reset_rainfall():
    global rain_count
    rain_count = 0

rain_sensor = Button(6)
rain_sensor.when_pressed = bucket_tipped

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
    while time.time() - start_time <= interval:
        wind_start_time = time.time()
        reset_wind()
        
        #time.sleep(wind_interval)
        while time.time() - wind_start_time <= wind_interval:
            store_directions.append(wind_direction_byo.get_value())

        final_speed = calculate_speed(wind_interval)
        store_speeds.append(final_speed)

    humidity, pressure, temperature = bme280_sensor.read_all()

    rainfall = rain_count * BUCKET_SIZE
    reset_rainfall()

    wind_direction_avg = wind_direction_byo.get_average(store_directions)
    wind_speed_max = max(store_speeds) # wind gust
    wind_speed_last = store_speeds[-1]
    wind_speed_avg = statistics.mean(store_speeds)

    readings_dict = {
        "timestamp_epoch" : currentEpoch(),
        "wind_direction_avg" : wind_direction_avg,
        "wind_speed_max" : wind_speed_max,
        "wind_speed_last" : wind_speed_last,
        "wind_speed_avg" : wind_speed_avg,
        "rainfall" : rainfall,
        "humidity" : humidity,
        "pressure" : pressure,
        "temperature" : temperature
    }

    msg = json.dumps(readings_dict)

    print(msg)
    publish(msg)

    # reset readings
    store_speeds = []
    store_directions = []
