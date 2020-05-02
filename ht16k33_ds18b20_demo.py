# file: ht16k33_ds18b20_demo.py
# date: 2020-05-02

import machine
import utime as time
from machine import Pin
import onewire, ds18x20
import ubinascii as binascii
import ht16k33

#----------------------------------------------

def read_temp(ds,addr): 
    ds.convert_temp()  # start temperature conversion
    time.sleep_ms(750)
    try:
       temp = ds.read_temp(addr) # temperature in Celsius
    except Exception: # CRC error
        return ''
    # assume the temperature value of human body is positive
    temp_str = '{:.1f}'.format(temp)
    return temp_str

def show_temp(ht, s):
    pos = 2 # set start position (column)
    for c in s:
        if c == '.': # decimal point
            data = [0x01]
        else: # digit
            data = ht16k33.DIGITS[int(c)]
        for b in data:
            ht.write(pos,b)
            pos += 1
        pos += 1
    ht.show()

#----------------------------------------------
# Use GPIO22=SCL, GPIO21=SDA
i2c = machine.I2C( freq=400000,
         scl=machine.Pin(22), sda=machine.Pin(21) )

ht = ht16k33.LED16X8(i2c)
ht.clear() # clear display 

#----------------------------------------------
# Use GPIO23 for DS18B20 (with 10k pullup on DATA pin)
pin = machine.Pin(23) 
ds = ds18x20.DS18X20(onewire.OneWire(pin))
addr_list = ds.scan() # scan DS18B20 devices 
print( 'Number of DS18B20 devices found:', len(addr_list) )
for addr in addr_list:
    print( binascii.hexlify(addr) ) # show unique 64-bit serial code

#----------------------------------------------

if len(addr_list) == 0:
    print('No device found !!!')
else:
    addr = addr_list[0]

try:
    while True:
        value_str = read_temp(ds, addr)
        show_temp(ht, value_str)
except KeyboardInterrupt:
    ht.shutdown()
finally:
    print('Done')


