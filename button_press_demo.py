# file: button_press_demo.py

from machine import Pin
import utime as time
from button import Button

# use GPIO21 pin for LED output 
LED_GPIO = const(21)
led = Pin( LED_GPIO, mode=Pin.OUT )

# use GPIO22 pin for external pushbutton (active-low)
BTN_GPIO = const(22)
btn = Pin( BTN_GPIO, mode=Pin.IN, pull=Pin.PULL_UP )
button = Button( btn )

press_cnt = 0
stop = False

def btn_press_cb(t):
    global press_cnt, stop
    press_cnt += 1
    if t==Button.LONG_PRESS: # long press
        led.value(0)
        stop = True
    elif t==Button.SHORT_PRESS: # short press
        led.value( not led.value() )
    print('button callbacks:', press_cnt )

# set callback functoin for the button pin 
button.on_pressed( callback=btn_press_cb )

# press Ctrl+C or long-press the button
try:
    ts = time.ticks_ms()
    while not stop:
        if button.was_long_pressed():
            print('long press')
        elif button.was_short_pressed():
            print('short press')            
        else:
            if time.ticks_diff(time.ticks_ms(), ts) >= 500:
                ts = time.ticks_ms()
                print( button.read() )
        time.sleep_ms(50)
except KeyboardInterrupt:
    pass
finally:
    button.deinit()
    print('Done')

