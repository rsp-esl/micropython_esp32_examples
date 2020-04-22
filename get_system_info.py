# file: get_system_info.py 
# -- show system information such as OS version, machine name, MAC addresses
# date: 2020-04-22

import uos as os
import utime as time
import network
import ubluetooth as bluetooth

def mac_to_str(mac):
    if isinstance(mac,bytes):
        mac = bytearray(mac)
    mac_str = ':'.join(['{:02X}'.format(x) for x in mac])
    return mac_str

# get system information
results = os.uname()
names = ['sysname', 'nodename', 'release', 'version', 'machine']
if len(names) == len(results):
   for name,value in zip(names,results):        
       print( "{}: {}".format(name,value) )

wlan=network.WLAN()
# get mac address (an array of 6 bytes)
mac_bytes = wlan.config('mac')
# convert 6-byte mac address to a hex string
print( 'WiFi MAC address: {}'.format(mac_to_str(mac_bytes)) )

ble = bluetooth.BLE()
ble.active(1)
mac_bytes = ble.config('mac')
# convert 6-byte mac address to a hex string
print( 'Bluetooth MAC address: {}'.format(mac_to_str(mac_bytes)) )
ble.active(0)

