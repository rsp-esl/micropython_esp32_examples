# file: pcf8574_demo-1.py
# date: 2020-05-05

from machine import Pin,I2C
import utime as time

# Use GPIO22=SCL, GPIO21=SDA
i2c = I2C( freq=100000,scl=Pin(22),sda=Pin(21) )
addr = 0x21
dev_found = addr in i2c.scan()
try:
    cnt = 0  # counter variable, set to 0
    data = bytearray(1) # one-byte data buffer
    while dev_found:
        data[0] = cnt ^ 0xff # invert bits
        # write to PCF8574
        i2c.writeto( addr, data )
        # increment counter by 1 
        cnt = (cnt+1) % 256
        time.sleep_ms(100)
except KeyboardInterrupt:
    pass
finally:
    print('Done')

