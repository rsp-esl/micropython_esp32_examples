# file: led_push_button_timer_thread.py 
# -- LED toggle using thread
# Date: 2020-04-22 

from machine import Pin, Timer
from micropython import const
import utime as time
import _thread

BTN_GPIO = const(22) # use GPIO-22 for push-button input
LED_GPIO = const(21) # use GPIO-21 for LED output

btn = Pin( BTN_GPIO, mode=Pin.IN, pull=Pin.PULL_UP )
led = Pin( LED_GPIO, mode=Pin.OUT )

stop = False # used as a global variable

def led_toggle(led): # thread function
    global stop
    state = 0
    while not stop:
        state = not state
        print( 'LED state: {}'.format( int(state) ))
        led.value(state)   # update LED output
        time.sleep_ms(100) # sleep for 0.1 seconds

# create and start a thread
_thread.start_new_thread( led_toggle, (led,) )

def stop_led_blink(timer): # callback function for timer
    global stop
    stop = True

TIMER_NUM = const(-1)      # virtual Timer
timer = Timer( TIMER_NUM ) # create a Timer object

# start the timer in one-shot mode
timer.init( period=5000, mode=Timer.ONE_SHOT, callback=stop_led_blink )
try: 
    # Press the button to stop and exit the loop
    while not stop:
        if btn.value() == 0: # check whether button is pressed
            stop = True
            break
        time.sleep_ms(10)
except KeyboardInterrupt:
    stop = True
    print('Terminated...')
finally:
    led.value(0)   # turn off LED
    timer.deinit() # stop timer
    print('Done')

