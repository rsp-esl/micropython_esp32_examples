# file: led_push_button_irq-2.py 
# -- LED toggle with stop push button (interrupt-driven)
# Date: 2020-04-22 

from machine import Pin
import utime as time

BTN_GPIO = const(22) # use GPIO-22 for push-button input
LED_GPIO = const(21) # use GPIO-21 for LED output

# create objects from machine.Pin
led = Pin( LED_GPIO, mode=Pin.OUT )
btn = Pin( BTN_GPIO, mode=Pin.IN, pull=Pin.PULL_UP )

btn_event_count = 0

def btn_handler(pin): # interrupt handler for Button pin
    global btn_event_count
    btn_event_count = btn_event_count+1

# enable interrupt handler for Button pin
btn.irq( handler=btn_handler, trigger=Pin.IRQ_FALLING )

state = False
stop  = False

try:
    while not stop:
        if btn_event_count > 0:
            state = not state  # toggle state
            led.value( state ) # update LED output
            cnt = 0
            # wait until the button is released
            while btn.value() == 0: 
                time.sleep_ms(50)
                cnt = cnt + 1
                if cnt > 20: # long pressed 
                    stop = True
                    break
            btn_event_count = 0
        else:
            time.sleep_ms(100)
except KeyboardInterrupt:
    print('Terminated...')
finally:
    btn.irq( handler=None )
    print('Done')

