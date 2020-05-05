# file: pcf8574_demo-2.py
# date: 2020-05-05

from machine import Pin,I2C
import utime as time

# Use GPIO22=SCL, GPIO21=SDA
i2c = I2C( freq=100000,scl=Pin(22),sda=Pin(21) )
addr = 0x20
dev_found = addr in i2c.scan()
try:
    # write 0xff to PCF8574 for input direction
    i2c.writeto( addr, bytes([0xff]) )
    while dev_found:
        # read 1 byte from PCF8574
        data = i2c.readfrom( addr, 1 )
        data = data[0]
        for i in range(3):
            if (data >> i) & 1 == 0:
                print('Button at P{} is pressed.'.format(i))
        time.sleep_ms(100)
except KeyboardInterrupt:
    pass
finally:
    print('Done')

