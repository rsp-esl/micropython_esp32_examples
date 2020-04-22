# file: i2c_device_scan.py 
# Date: 2020-04-22 

import machine, utime

# Use GPIO22=SCL, GPIO21=SDA 

i2c_bus = 0 # use bus 0 or 1
i2c = machine.I2C( i2c_bus, freq=400000,
    scl=machine.Pin(22), sda=machine.Pin(21) )

devices   = i2c.scan()  # scan I2C devices
num_found = len(devices)

if num_found > 0:
    print('I2C device%s found: ' % ('s' if num_found > 1 else ''))
    cnt = 1
    for dev in devices:
        print('({}) addr: {}'.format(cnt, hex(dev)))
        cnt = cnt+1
    print('')
else:
    print('no I2C devices found')

