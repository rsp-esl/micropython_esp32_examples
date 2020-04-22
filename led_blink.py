# file: led_blink.py
# -- LED blink using GPIO2 pin for LED output 
# Date: 2020-04-22

from machine import Pin
import utime as time
from micropython import const

# use GPIO-2 pin (onboard 'Blue' LED)
LED_GPIO = const(2) # create a constant for integer literal

# create an object from machine.Pin (digital output pin)
led = Pin( LED_GPIO, Pin.OUT )

state = False
STATUS = ['OFF','ON']
try:
    while True:
        state = not state # toggle state
        print( 'LED: {}'.format( STATUS[int(state)] ) )
        led.value(state)  # write value to output pin
        time.sleep(0.5)   # sleep for a half second
except KeyboardInterrupt:
    print('Terminated...')

