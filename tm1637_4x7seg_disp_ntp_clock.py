# file: tm1637_4x7seg_disp_ntp_clock.py
# -- digital clock with tm1637 4-digit segment display and NTP time sync.
# date: 2020-04-22

from machine import Pin, RTC
from micropython import const
import network, os
import usocket as socket
import utime as time
import ustruct as struct
import tm1637
import _thread

# Specify the SSID and password of your WiFi network
WIFI_CFG = { 'ssid': "XXXX", 'password': "XXXXX" }

NTP_HOST = "th.pool.ntp.org"

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

def get_ntp_time( ntp_host, ntp_port=123, timeout=5 ):
    ntp_data = bytearray(48)
    ntp_data[0] = 0x1b
    addr = socket.getaddrinfo(ntp_host, ntp_port)[0][-1]
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    seconds = 0
    try:
        s.settimeout( timeout )
        res = s.sendto( ntp_data, addr )
        msg = s.recv(48)
        seconds = struct.unpack("!I", msg[40:44])[0]
    except OSError as ex:
        pass
    finally:
        s.close()
    # epoch time in seconds since Jan 1, 1900 00:00:00 UTC
    return seconds

def set_rtc( tm ):
    year, month, day, hour, min, sec, wday, yday = tm
    print( year, month, day, hour, min, sec, wday, yday )
    RTC().datetime( (tm[0],tm[1],tm[2],tm[6]+1,tm[3],tm[4],tm[5],0) )

def show_digital_clock(disp):
    cnt = 0
    while True:
        tm = RTC().datetime()
        hh, mm = tm[4],tm[5]
        cnt ^= 1
        if cnt == 0:
           disp.numbers(hh,mm)
        else:
           disp.show('{0:02d}{1:02d}'.format(hh,mm))
        time.sleep_ms(500)

CLK = const(4) # use GPIO-4 for CLK pin
DIO = const(0) # use GPIO-0 for DIO pin

disp = tm1637.TM1637(clk=Pin(CLK), dio=Pin(DIO))
disp.brightness(7) # set brightness level: 0..7
disp.show('----')

rtc_ntp_sync = False

if connect_wifi( WIFI_CFG ):
    ts = get_ntp_time( NTP_HOST )
    if ts > 0:
        # 3155673600 sec = (date(2000,1,1) - date(1900,1,1)) * (24*60*60)
        tm = time.localtime( ts - 3155673600 + 25200 ) # GMT+7
        set_rtc( tm )
        rtc_ntp_sync = True
    else:
        print('NTP error')
else:
    print('Network error')

if rtc_ntp_sync:
    _thread.start_new_thread ( show_digital_clock, (disp,) )

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    _thread.exit() # stop threads
finally:
    print('Done')

