# file: wifi_scan-1.py 
# Date: 2020-04-22 

import network
import utime as time

# open WiFi interface in STA mode 
wifi = network.WLAN( network.STA_IF )

# activate the WiFi interface (if_up)
wifi.active(True)

print ('Press Ctrl+C to stop WiFi scanning...')
while True:
    try:
        # scan WiFi and get the results as a list of tuples
        scan_results = wifi.scan()
        # print scan results
        print(60*'=')
        for ap in scan_results:
            print( ap )
        print(60*'-')
    except KeyboardInterrupt:
        print('Terminated...')
        break

# deactivate the WiFi interface
wifi.active(False)

