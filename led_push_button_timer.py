# file: led_push_button_timer.py 
# LED toggle using software timer 
# Date: 2020-04-22 

from machine import Pin, Timer
from micropython import const
import utime as time

BTN_GPIO = const(22) # use GPIO-22 for push-button input
LED_GPIO = const(21) # use GPIO-21 for LED output

btn = Pin( BTN_GPIO, mode=Pin.IN, pull=Pin.PULL_UP )
led = Pin( LED_GPIO, mode=Pin.OUT )

def led_toggle(timer):
    global led
    # show elapsed system time in msec
    print( 'timer ticks: {} msec'.format(time.ticks_ms()) )
    led.value( not led.value() )
    
TIMER_NUM = const(-1)      # virtual Timer
timer = Timer( TIMER_NUM ) # create a Timer object

# use the timer in periodic mode (period = 500 msec)
timer.init( period=500, mode=Timer.PERIODIC, callback=led_toggle )

try:
    # Press the button to stop and exit the loop
    while True:
        # check whether button is pressed or not
        if btn.value() == 0: 
            break
        time.sleep_ms(10)
except KeyboardInterrupt:
    print('Terminated...')
finally:
    timer.deinit() # stop timer
    print('Done')

