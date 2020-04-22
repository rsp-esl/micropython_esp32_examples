# file: wifi_worldtime_http_get.py 
# Date: 2020-04-22 

import network
import utime as time
import ujson as json
import urequests as requests

# Specify the SSID and password of your WiFi network
WIFI_CFG = { 'ssid': "XXXX", 'password': "XXXXXXX" }

def connect_wifi( wifi_cfg, max_retries=10 ):
    # use WiFi in station mode (not AP)
    wifi_sta = network.WLAN( network.STA_IF )
    # activate the WiFi interface (up)
    wifi_sta.active(True)
    # connect to the specified WiFi AP
    wifi_sta.connect( wifi_cfg['ssid'], wifi_cfg['password']  )
    retries = 0
    while not wifi_sta.isconnected():
        retries = retries + 1
        if retries >= max_retries:
            return None
        time.sleep_ms(200)
    return wifi_sta

def get_worldtime_data( url ):
    resp = requests.get( url )
    if resp.status_code == 200:  # request ok
        try:
            data = json.loads( resp.text )
        except Exception as ex:
            print ('JSON data error...' )
            return 
        print( 'Timezone:', data['timezone'] )
        print( 'Epoch time (Jan 1, 1970):', int(data['unixtime']) ) 
        print( 'UTC   datetime:', data['utc_datetime'] )
        print( 'Local datetime:', data['datetime'] )
        print( 'UTC offset   (hours):', data['utc_offset'] )
        print( 'UTC offset (seconds):', int(data['raw_offset']) )
    else:
        print ('HTTP request error...')
    
# try to connect the network
wifi = connect_wifi( WIFI_CFG )
print( network.WLAN().ifconfig() )

URL = "http://worldtimeapi.org/api/timezone/Asia/Bangkok"
if wifi is not None:
    get_worldtime_data( URL )
else:
    print('No WiFi connection')

