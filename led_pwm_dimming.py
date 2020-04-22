# file: led_pwm_dimming.py
# PWM-based LED dimming (brightness adjustment)
# Date: 2020-04-22 

from machine import Pin, PWM
import utime as time
from micropython import const
import math

BTN_GPIO = const(22) # use GPIO-22 for push-button input
LED_GPIO = const(21) # use GPIO-21 for LED output

btn = Pin( BTN_GPIO, mode=Pin.IN, pull=Pin.PULL_UP )
led = Pin( LED_GPIO, mode=Pin.OUT )

# create an object from PWM for the LED pin
pwm = PWM( led, freq=1000, duty=0 )
time.sleep_us(10)

print ('PWM freq: {} Hz'.format( pwm.freq() ))
N = const(32)
for i in range(N+1):
    if btn.value() == 0: # check whether button is pressed
        break
    value = int(1023*math.sin(math.pi*i/N))
    pwm.duty( value )  # set the duty cycle value 
    time.sleep_ms( 100 )
    percent = 100*( pwm.duty()/1024.0 )
    print( 'Duty cycle: {:4d} ({:4.1f}%)'.format(value, percent) )

pwm.duty(0)
pwm.deinit() # important: turn off the PWM pin

