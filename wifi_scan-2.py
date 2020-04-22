# file: wifi_scan-2.py 
# Date: 2020-04-22 

import network
import ujson as json

param_names = ['essid','mac','channel','rssi','authmode','hidden']
authmodes = ['OPEN','WEP','WPA-PSK','WPA2-PSK','WPA/WPA2-PSK','MAX']

def mac_bytes_to_hex_str(mac_bytes):
    return ':'.join( ['%02X' % x for x in mac_bytes])

def convert_to_json( found_list ):
    results = { 'count': len(found_list), 'found_list': [] }
    for ap in found_list:
        pairs = dict(zip(param_names,ap))
        for name in pairs:
            value = pairs.get(name)
            if type(value).__name__=='bytes':
                if name=='mac' and len(value)==6:
                    value = mac_bytes_to_hex_str( value )
                else:
                    value = value.decode('ascii')
            else:
                try:
                    value = int(value)
                    if name=='authmode' and 0 <= value <= 5:
                        value = authmodes[value]
                except (ValueError, TypeError):
                    pass
            pairs[name] = value
        results['found_list'].append( pairs )
    return results

# open WiFi interface in STA mode 
wifi = network.WLAN( network.STA_IF )

# activate the WiFi interface
wifi.active(True)

# scan WiFi and get the results as a list of tuples
scan_results = wifi.scan()

# deactivate the WiFi interface
wifi.active(False)

# convert a list of tuples to json data
results = convert_to_json( scan_results )

n = results.get('count')
if n > 0:
    for item in results.get('found_list'):
        print( json.dumps(item) )
else:
    print( 'No WiFi found' )

