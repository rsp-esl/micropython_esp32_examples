# file: ntp_rtc_sync.py
# -- Synchronize the RTC with NTP server 
# date: 2020-04-22

import network
import ujson as json
from machine import RTC
import utime as time
import ntptime

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

while True:
    try:
        # synchronize RTC with NTP server
        ntptime.settime()
        break
    except OSError:
        print('NTP server: connection timeout...')

# create an RTC object
rtc = RTC()

# read current datetime from RTC
year, month, day, wday, hour, minute, second, _ = rtc.datetime()

# 0=Mon, 1=Tue, ...
week_days = ['Mon','Tue','Wed','Thu','Fri','Sat','Sun' ]

# show current date
print( '{} {}/{}/{}'.format(week_days[wday],day,month,year) )

# show current time (GMT+7)
print( '{}:{}:{}'.format(hour+7, minute, second) )

# disenable WiFi 
wifi.active(False)

