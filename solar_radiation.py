from pysolar.solar import *
from pytz import timezone
import datetime

def get_solar_details(lat, long):
    date = datetime.datetime.now(timezone('US/Eastern'))
    alt = get_altitude(lat, long, date)
    az = get_azimuth(lat, long, date)
    rad = radiation.get_radiation_direct(date, alt)
    return alt, az, rad