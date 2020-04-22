# file: led_push_button_irq-1.py 
# -- LED toggle with stop push button (interrupt-driven)
# Date: 2020-04-22 

from machine import Pin
from micropython import const
import utime as time

BTN_GPIO = const(22) # use GPIO-22 for push-button input
LED_GPIO = const(21) # use GPIO-21 for LED output

# create objects from machine.Pin
led = Pin( LED_GPIO, mode=Pin.OUT )
btn = Pin( BTN_GPIO, mode=Pin.IN, pull=Pin.PULL_UP )

def btn_handler(pin): # interrupt handler for Button pin
    global stop
    print( pin, pin.value() )
    stop = True

# enable interrupt handler for Button pin
btn.irq( handler=btn_handler, trigger=Pin.IRQ_FALLING )

stop  = False
state = False
try:
    while True:
        if stop:
            led.value(0)    # turn off the LED
            break           # exit loop
        state = not state   # toggle state
        led.value( state )  # write value to output pin
        time.sleep_ms(100)  # sleep for 0.1 seconds
except KeyboardInterrupt:
    print('Terminated...')
finally:
    btn.irq( handler=None )
    print('Done')

