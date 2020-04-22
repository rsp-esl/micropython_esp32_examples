# file: led_push_button_poling.py
# -- LED toggle with stop push button
# Date: 2020-04-22 

from machine import Pin
from micropython import const
import utime as time

BTN_GPIO = const(22) # use GPIO-22 for push-button input
LED_GPIO = const(21) # use GPIO-21 for LED output

# create objects from machine.Pin
led = Pin( LED_GPIO, mode=Pin.OUT )
btn = Pin( BTN_GPIO, mode=Pin.IN, pull=Pin.PULL_UP )
state = False # used to keep the output state

try:
    while True:
        # check whether button is pressed or not
        if btn.value() == 0: 
            break           # exit loop
        state = not state   # toggle state
        led.value( state )  # write value to output pin
        time.sleep_ms(100)  # sleep for 0.1 seconds
except KeyboardInterrupt:
    print('Terminated...')
finally:
    print('Done')

