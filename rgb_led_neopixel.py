# file: rgb_led_neopixel.py
# -- RGB LED (Neopixel) color setting
# Date: 2020-04-22 

from machine import Pin
from neopixel import NeoPixel
import utime as time

GPIO_NUM = const(23) # use GPIO-23
pin = Pin( GPIO_NUM, Pin.OUT ) # create a Pin object 

NUM_PIXELS = const(1) # 'only one' RGB LED in the strip
np = NeoPixel( pin, NUM_PIXELS ) # create a Neopixel object

colors = [(255,0,0),(0,255,0),(0,0,255)] # red, green, blue

for color in colors:
    np[0] = color   # set color value to the first RGB LED
    np.write()      # apply the color value
    time.sleep_ms(1000)

np[0] = (0,0,0)     # turn off color (black)
np.write()

