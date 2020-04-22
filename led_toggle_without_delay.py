# file: led_toggle_without_delay.py
# date: 2020-04-22

from machine import Pin
from micropython import const
import utime as time

LED_GPIO = const(2)
led = Pin(LED_GPIO, Pin.OUT)

interval = const(100)
prev_tick_msec = 0

def toggle(p):
    p.value(not p.value() ) # toggle pin

try:
    while True:
        now = time.ticks_ms()
        if now - prev_tick_msec > interval:
            prev_tick_msec = now
            toggle( led )
except KeyboardInterrupt:
    print('Terminated')
finally:
    print('Done')

