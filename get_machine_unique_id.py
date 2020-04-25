# file: get_machine_unique_id.py 
# date: 2020-04-24

import machine
import ubinascii as binascii

# get unique ID (MAC address) of the device 
id_bytes = machine.unique_id()
bb = bytearray(id_bytes)

mac_str = ':'.join('{:02X}'.format(x) for x in bb) 
print( 'MAC address:', mac_str )

node_id = binascii.hexlify(id_bytes).decode('utf-8')
print( node_id.upper() )

