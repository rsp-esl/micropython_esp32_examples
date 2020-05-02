# file: ht16k33_demo.py
# date: 2020-05-02

import machine
import utime as time
import ht16k33

# Use GPIO22=SCL, GPIO21=SDA
i2c = machine.I2C( freq=400000,
         scl=machine.Pin(22), sda=machine.Pin(21) )

ht = ht16k33.LED16X8(i2c)

ht.shutdown(False) # enter normal mode
ht.clear()         # clear display 
ht.brightness(7)   # set brightness to 7
ht.display_on()    # turn of display

cnt = 0 # counter variable
try:
    while True:
        t = cnt
        for pos in [12,8,4,0]:
            i = pos
            digit = t%10
            for b in ht16k33.DIGITS[digit]:
                ht.write(i,b) 
                i += 1 
            t //= 10
        for i in range(-16,16):
            ht.show(i)             
            time.sleep_ms(150)
        cnt = (cnt+1) % 10000 # increment by 1

except KeyboardInterrupt:
    ht.shutdown()
finally:
    print('Done')

