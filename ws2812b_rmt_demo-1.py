# File: ws2812b_rmt_demo-1.py
# Date: 2020-05-27

from machine import Pin
import esp32
import utime as time

WS2812B_PIN = Pin(27)

# create an RMT object, use clock divider = 8
# => The resolution is 100ns or 0.1us
rmt = esp32.RMT(id=0, pin=WS2812B_PIN, clock_div=8)

# define bit timings: pulse widths 
BIT0 = (4,8) # T0H = 0.4us, T0L = 0.8us
BIT1 = (8,4) # T1H = 0.8us, T1L = 0.4us

# test colors
RED_COLOR   = 8*BIT0 + 8*BIT1 + 8*BIT0
GREEN_COLOR = 8*BIT1 + 8*BIT0 + 8*BIT0
BLUE_COLOR  = 8*BIT0 + 8*BIT0 + 8*BIT1
COLORS = [RED_COLOR, GREEN_COLOR, BLUE_COLOR]

try:
    # press Ctrl+C to terminate
    while True: # main loop 
        for bits in COLORS:
            # send data to RMT
            rmt.write_pulses( bits, start=1)
            # wait until RMT done
            rmt.wait_done()
            time.sleep(1.0)
except KeyboardInterrupt:
    print('Terminated...')
finally:
    rmt.deinit() # release the RMT channel


