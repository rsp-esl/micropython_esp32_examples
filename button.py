# file: button.py 

import machine
from machine import Pin
import utime as time

_PRESS_MIN_MSEC = [80,800]
  
class Button():
    LONG_PRESS  = 1
    SHORT_PRESS = 0
    
    def __init__(self,pin):
        self._pin = pin
        pin_trigger = Pin.IRQ_RISING | Pin.IRQ_FALLING 
        self._pin.irq( handler=self._pin_handler,trigger=pin_trigger)
        self._state = self._pin.value()
        self._ts = time.ticks_ms()
        self._pressed_cb = None
        self._was_long_pressed  = False
        self._was_short_pressed = False

    def on_pressed(self,callback):
        self._pressed_cb = callback

    def _pin_handler(self, pin):
        ticks = time.ticks_ms()
        new_state = pin.value()
        is_up   = self._state == 0 and new_state == 1
        is_down = self._state == 1 and new_state == 0
        self._state = new_state
        if is_up:
            dt = time.ticks_diff(ticks, self._ts)
            if dt > _PRESS_MIN_MSEC[0] and self._pressed_cb:
               if dt > _PRESS_MIN_MSEC[1]:
                   self._was_long_pressed = True
                   self._pressed_cb(Button.LONG_PRESS)
               else:
                   self._was_short_pressed = True
                   self._pressed_cb(Button.SHORT_PRESS)
        elif is_down:
            self._ts = ticks

    def was_long_pressed(self):
        if self._was_long_pressed:
            self._was_long_pressed = False
            return True
        return False

    def was_short_pressed(self):
        if self._was_short_pressed:
            self._was_short_pressed = False
            return True
        return False
    
    def read(self):
        return self._pin.value()

    def deinit(self):
        self._pin.irq(handler=None)

