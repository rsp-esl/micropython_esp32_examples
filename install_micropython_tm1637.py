# file: install_micropython_tm1637.py
# -- install micropython-tm1637 package 
# see: https://github.com/mcauser/micropython-tm1637
# date: 2020-04-22

import network
import uos
import utime as time
import upip as pip

# Specify the SSID and password of your WiFi network
WIFI_CFG = { 'ssid': "XXXXX", 'password': "XXXXXXXX" }

def connect_wifi( wifi_cfg, retries = 10 ):
    wifi_sta = network.WLAN( network.STA_IF )
    wifi_sta.active(True)
    wifi_sta.connect( wifi_cfg['ssid'], wifi_cfg['password'] )
    while not wifi_sta.isconnected():
        retries -= 1 
        if retries < 0:
            return None
        time.sleep(1.0)
    return wifi_sta

if connect_wifi( WIFI_CFG ):
    # install micropython-tm1637 to /lib 
    pip.install('micropython-tm1637', '/lib')
    # list the /lib directory
    print( os.listdir('/lib') ) 

