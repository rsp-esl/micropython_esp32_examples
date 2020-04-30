# file: tm1638_demo-1.py
# date: 2020-04-30

import tm1638
from machine import Pin
import utime as time
import math

tm = tm1638.TM1638(stb=Pin(23), clk=Pin(22), dio=Pin(21))
tm.clear()
tm.brightness(4)

x = int(math.pi*10e6)
for i in range(8):
    value = tm1638.DIGITS[ x%10 ]
    if i==7:
        value |= 0x80 # show dot (DP)
    tm.segment( 7-i, value )
    x //= 10
	
time.sleep(3.0)
tm.off()
del tm

