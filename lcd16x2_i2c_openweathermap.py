# file: lcd16x2_i2c_openweathermap.py
# date: 2020-04-25

import network
import machine
from machine import Pin
import utime as time
import ujson as json
import urequests as requests
from lcd_pcf8574 import LCD

# URL and APPID for openweathermap
API_URL = 'https://api.openweathermap.org/data/2.5/weather'
APPID   = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx' # Specify your APPID

#---------------------------------------------------------
# Step 1) Connect WiFi
# read the configuration data from wifi_config.json

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

#---------------------------------------------------------
# Step 2) get weather data from OpenWeatheMap

def get_weather( APPID, city ):
    results = {}
    url = API_URL + '?units=metric&APPID=' + APPID + '&q=' + city
    try:
        data = requests.get(url).json()
    except OSError:
        print ('Cannot get data from OpenWeatherMap..')
        return results
    code = data.get('cod')
    #print( json.dumps(data) )
    
    if code == 200: # response OK
        city = data['name']
        results['p'] = data['main']['pressure'] # hPa
        results['t'] = data['main']['temp']     # deg.C
        results['h'] = data['main']['humidity'] # %
    elif code == 401:
        print('Error Code:', code)
        print( data['message'] )
    return results

city_name = 'Nonthaburi,TH'
results = get_weather( APPID, city_name )

#---------------------------------------------------------
# Step 3) Display weather data on LCD16x2 I2C

# Use GPIO22=SCL, GPIO21=SDA
i2c_bus = 0 # use bus 0 or 1
i2c = machine.I2C( i2c_bus, freq=400000,
    scl=machine.Pin(22), sda=machine.Pin(21) )
# use I2C address = 0x3f
lcd = LCD(i2c, 0x3f)

weather_data = {
    't': ('Temperature','deg.C'),
    'h': ('Humidity','%'),
    'p': ('Pressure','hPa'), }

try:
   while True:
       for key in weather_data:
           lcd.clear() # clear display
           lcd.goto_line( 0 )     # goto the first line
           lcd.print( city_name ) # show city name
           lcd.goto_line( 1 ) # goto the second line
           name, unit = weather_data[key]
           value = results[key]
           lcd.print('{}: {} {}'.format(name,value,unit) )
           time.sleep_ms(2000)
           for i in range(16):
              lcd.write_cmd(0x10 | 0x08) # shift display to left
              time.sleep_ms(500)
except KeyboardInterrupt:
    lcd.clear()
finally:
    print('Done')


