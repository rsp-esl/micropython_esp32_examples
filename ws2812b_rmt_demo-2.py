# File: rmt_ws2812b_demo-2.py
# Date: 2022-05-27

from machine import Pin
import utime as time
from ws2812b import WS2812B

WS2812B_PIN = Pin(27)
NUM_LEDS    = 8

# create WS2812B object for n-pixel RGB LED strip
strip = WS2812B(pin=WS2812B_PIN,n=NUM_LEDS)

# define test colors
COLORS = [
    0x3f << 16, 0x3f << 8, 0x3f,
     0x3f3f00, 0x3f003f, 0x003f3f,
    0x7f7f7f,(127,20,20) ]

try:
    for i in range(NUM_LEDS):
        strip[i] = COLORS[i]
    strip.update()
    time.sleep_ms(500)
    
    # press Ctrl+C to terminate
    while True: # main loop
        for i in range(16):
            if i < 8:
                # rotate shift left
                strip.shift_left()
            else:
                # rotate shift right
                strip.shift_right()
            strip.update()
            time.sleep_ms(1000)
except KeyboardInterrupt:
    print('Terminated...')
finally:
    strip.clear()
    strip.deinit() # release the RMT channel


