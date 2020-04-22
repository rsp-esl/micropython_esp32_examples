# file: i2c_bh1750_light_sensor_reading.py 
# Date: 2020-04-22 

import machine, utime

i2c_bus = 0 # use bus 0 or 1
i2c = machine.I2C( i2c_bus, freq=400000,
    scl=machine.Pin(22), sda=machine.Pin(21) )

def bh1750_init(addr):
    try:
        # power on the BH1750
        i2c.writeto(addr, bytes([0x01]) )
        # reset the BH1750
        i2c.writeto(addr, bytes([0x07]) )
        utime.sleep_ms(200)
        # set mode to 1.0x high-resolution, continuous measurement
        i2c.writeto(addr, bytes([0x10]) )
        utime.sleep_ms(150)
        return True
    except OSError as ex:
        return False

def bh1750_read(addr):
    try:
        data  = i2c.readfrom(addr, 2) # read two bytes
        value = (data[0]<<8 | data[1])/(1.2)
        return value
    except OSError as ex:
        print('BH1750 reading error')
        return None

if bh1750_init(0x23):
    for i in range(10): # repeat 10 times
        value = bh1750_read(0x23)
        print( 'Light level: [{0:>7.1f}] lx'.format(value) )
        utime.sleep_ms(500)
    print('Done')
else:
    print('BH1750 not found...')

