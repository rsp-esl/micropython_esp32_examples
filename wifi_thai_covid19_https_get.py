# file: wifi_thai_covid19_https_get.py 
# Date: 2020-04-22 

import network
import utime as time
import urequests as requests

# Specify the SSID and password of your WiFi network
WIFI_CFG = { 'ssid': "XXXXX", 'password': "XXXXXXXX" }

URL = "https://covid19.th-stat.com/api/open/today"

COVID19_NAMES = [
    ('Confirmed',    u'ยอดผู้ป่วยสะสม'),
    ('Recovered',    u'ผู้ป่วยรักษาหายแล้ว'),
    ('Hospitalized', u'ผู้ป่วยรักษาตัวในโรงพยาบาล'),
    ('Deaths',       u'ผู้เสียชีวิตสะสม'),
    ('NewConfirmed', u'ผู้ป่วยตรวจพบเพิ่มวันนี้'),
    ('NewRecovered', u'ผู้ป่วยรักษาหาย'),
    ('NewDeaths',    u'ผู้เสียชีวิตวันนี้'),
    ('UpdateDate',   u'อัปเดตล่าสุด')
]

def get_covid19_data( url ):
    data = None
    try:
        resp = requests.get( url )
        data = resp.json()
        for name in COVID19_NAMES[:-1]:
            if name[0] in data:
                value = str(data[name[0]])
                print('{}:\t\t\t\t{}'.format(name[1],value) )
        name = COVID19_NAMES[-1]
        update = data[ name[0] ]
        print( '{}: {}'.format(name[1], update)  )
    except Exception as ex:
        print('error...')
    return data

def connect_wifi( wifi_cfg ):
    wifi_sta = network.WLAN( network.STA_IF )
    wifi_sta.active(True)
    wifi_sta.connect( wifi_cfg['ssid'], wifi_cfg['password']  )
    while not wifi_sta.isconnected():
        time.sleep(1.0)

connect_wifi( WIFI_CFG )
get_covid19_data( URL )

