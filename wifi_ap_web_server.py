# file: wifi_ap_web_server.py 
# Date: 2020-04-22 

import network
import utime as time 
import usocket as socket
from machine import Pin

WIFI_OPEN = False 

if WIFI_OPEN: 
    AP_CFG = { 'essid': 'MyAP', 
           'authmode': network.AUTH_OPEN, 'channel':11, }
else:
    AP_CFG = { 'essid': 'MyAP', 'password': '@12345678', 
           'authmode': network.AUTH_WPA2_PSK, 'channel':11, }

def start_wifi_ap( ap_cfg ):
    # open WiFi in AP mode
    ap = network.WLAN( network.AP_IF )
    # activate AP interface (up)
    ap.active(True)
    # configure the AP interface
    try:
        # essid=ap_ssid, password=ap_password, authmode=ap_authmode
        ap.config( **ap_cfg )
    except Exception as ex:
        print ( 'Cannot set AP configuration...' )
    if ap.active():
       return ap
    else:
       return False

def start_web_server( btn=None ):
    global sock
    # create a socket (STREAM TCP socket) for network connection
    sock = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
    # set socket option: reuse address
    sock.setsockopt( socket.SOL_SOCKET, socket.SO_REUSEADDR, 1 )
    # use socket in non-blocking mode
    sock.setblocking( False )
    # get server address
    addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
    # bind the socket to port 80 (HTTP)
    sock.bind( addr )
    # listen for an incoming connection
    sock.listen(1)
    while True:
        try:
            conn, addr = sock.accept() # waiting for connection
        except OSError:
            if btn and btn.value()==0:
               sock.close() # close socket
               break        # break the loop
            else:
               continue
        request = conn.recv(1024) # read incoming request data
        print( 'Content = %s' % str(request) )
        # send HTML as response
        html = '<html><head></head><body>'
        html += '<h1>Welcome to ESP32...</h1><br>'
        html += '<b>Client from {}<b><br>'.format(str(addr))
        html += '</body></html>'
        conn.send( html ) 
        conn.close() # close HTTP connection
        time.sleep_ms(10)

sock = None
ap = start_wifi_ap( AP_CFG )
ipaddr = ap.ifconfig()[0]
print ( 'IP address:', ipaddr ) # 192.168.4.1

BTN_GPIO = const(23)    # use GPIO23 for push button
btn = Pin( BTN_GPIO, Pin.IN, Pin.PULL_UP )

try:
   start_web_server( btn ) # start web server
except KeyboardInterrupt:
    pass
finally:
    if sock:
        sock.close()
    ap.active(False) # turn off WiFi AP

