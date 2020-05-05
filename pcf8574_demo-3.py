# file; pcf8574_demo-3.py
# date: 2020-05-05

from machine import Pin, I2C
from pcf8574 import PCF8574_BUTTONS, PCF8574_LED_BAR
import utime as time

# Use GPIO22=SCL, GPIO21=SDA
i2c = I2C( freq=100000, scl=Pin(22), sda=Pin(21) )

for addr in i2c.scan():
    print( hex(addr ) )

pcf_buttons = PCF8574_BUTTONS( i2c,0x20, Pin(23) )
pcf_leds    = PCF8574_LED_BAR( i2c,0x21, 0xfe    )

direction = 0
running = True
ts = time.ticks_ms()
try:
    while True:
        # read input from buttons (A,B,C)
        if pcf_buttons.pin_changed():
            clicked = pcf_buttons.button_clicked()
            btn_a = clicked[0]
            btn_b = clicked[1]
            btn_c = clicked[2]
            if btn_a: # exit the loop
                break
            elif btn_b and running:
                # change shift direction (left/right)
                direction = int(not direction)
            elif btn_c: # toggle running/paused
                running = not running
                
        # update output every 150 msec
        if time.ticks_diff(time.ticks_ms(), ts) >= 150:
            ts = time.ticks_ms() 
            pcf_leds.update()
            if running and direction==0:
                pcf_leds.rotate_left()
            elif running and direction==1:
                pcf_leds.rotate_right()
                
except KeyboardInterrupt:
    pass
finally:
    pcf_buttons.set_callback(None)
    pcf_buttons.deinit()
    pcf_leds.deinit()
    print('Done')

