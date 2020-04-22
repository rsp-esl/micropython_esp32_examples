# file: micropython_tm1637_demo.py
# -- Micropython-TM1637 demo 
# date: 2020-04-22

from machine import Pin
from micropython import const
import utime as time
import tm1637

CLK = const(4) # use GPIO-4 for CLK pin
DIO = const(0) # use GPIO-0 for DIO pin
tm = tm1637.TM1637(clk=Pin(CLK), dio=Pin(DIO))

tm.brightness(7) # set brightness level: 0..7

try:
    # show "12:34" with blinking colon
    show_colon = 0x00
    for i in range(10):
        tm.write([0x06, 0x5B | show_colon, 0x4F, 0x66])
        show_colon ^= 0x80
        time.sleep_ms(500)
    # show some words
    for word in ['help','fail','cool','----','24*C']:
        tm.show( word )
        time.sleep_ms(1000)
    # press Ctrl+C to stop
    for x in range(10000): # show 0000 to 9999
        tm.show( '{:04d}'.format(x) )
        time.sleep_ms(100)
except KeyboardInterrupt:
    pass
finally:
    print('Done')

