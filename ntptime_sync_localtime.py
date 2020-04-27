# ntptime_sync_localtime.py 
# date: 200-04-27

from machine import Pin, RTC
from micropython import const
import utime as time
import ujson as json
import network
import ntptime

# Step 1: connect WiFi

wifi_config = None
try:
    # read json file 'wifi_config.json' for WiFi configuration:
    #   { "ssid": "XXXXX", "password": "XXXXXXXX" }
    with open( 'wifi_config.json' ) as f:
        wifi_config = json.load(f)
except OSError:
    print('Cannot open configuration file')

def connect_wifi( wifi_cfg, retries=10 ):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect( wifi_cfg['ssid'], wifi_cfg['password'] )
    while not wlan.isconnected():
        retries -= 1
        if retries < 0:
           return None
        time.sleep_ms(1000)
    return wlan

wifi = connect_wifi( wifi_config ) 
if wifi is None:
    print('WiFi connection failed...')
    while True:
        pass

def ntp_sync_tz_offset( tz_offset=0 ):
    ntptime.settime()
    tm = time.localtime() 
    # print (tm)
    # tm[0] = year
    # tm[1] = month
    # tm[2] = day
    # tm[3] = hours
    # tm[4] = minutes
    # tm[5] = seconds
    # tm[6] = microseconds
    # tm[7] = day of year
    ts = time.mktime(tm) + (tz_offset)*60*60
    tm = time.localtime(ts)
    # (year, month, day, weekday, hours, minutes, seconds, subseconds)
    rtc_tm = tm[0:3] + (0,) + (tm[3],) + tm[4:6] + (0,)
    RTC().datetime(rtc_tm)

ntp_sync_tz_offset(7) # GTM+7
print ('Current datetime (Bangkok):', time.localtime())
print('Done')

