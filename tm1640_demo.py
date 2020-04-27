# file: tm1640_demo.py
# date: 2020-04-27

from machine import Pin, RTC
from micropython import const
import utime as time
import ujson as json
import network
import ntptime
from tm1640 import TM1640_LED_Matrix

#----------------------------------------------------------
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

#----------------------------------------------------------
# Step 2: connect NTP server and synchronize RTC with NTP

while True:
    try:
        # synchronize RTC with NTP server
        ntptime.settime()
        break
    except OSError:
        print('NTP server: connection timeout...')

# create an RTC object
rtc = RTC()

#----------------------------------------------------------
# step 3: display clock (hours and minutes)

DIGITS = [
    [0x7f,0x41,0x7f], # 0
    [0x21,0x7f,0x01], # 1
    [0x4f,0x49,0x79], # 2
    [0x49,0x49,0x7f], # 3
    [0x78,0x08,0x7f], # 4
    [0x79,0x49,0x4f], # 5
    [0x7f,0x49,0x4f], # 6
    [0x40,0x40,0x7f], # 7
    [0x7f,0x49,0x7f], # 8
    [0x79,0x49,0x7f]  # 9
]

DIO = const(0)
SCK = const(4)
sck_pin = Pin( SCK, Pin.OUT, value=0 )
dio_pin = Pin( DIO, Pin.OUT, value=0 )

disp = TM1640_LED_Matrix(sck_pin, dio_pin)
disp.brightness(7)

try:
    while True:
        # read current datetime from RTC
        tm = rtc.datetime()
        tz_offset = +7
        hour, minute = (tm[4]+tz_offset) % 24, tm[5]
        disp.write( DIGITS[hour//10], 0 )
        disp.write( DIGITS[hour%10],  4 )
        disp.write( [0x14], 7 ) # show colon
        disp.write( DIGITS[minute//10], 9 )
        disp.write( DIGITS[minute%10], 13 )
        time.sleep_ms(500)
        disp.write( [0x00], 7 ) # clear colon
        time.sleep_ms(500)
     
except KeyboardInterrupt:
    pass
finally:
    disp.clear()
    print('Done')
