# file: lcd16x2_pcf8574_demo-1.py
# date: 2020-04-23

import machine
import utime as time
from lcd_pcf8574 import LCD
import dht

# create a DHT22 object
dht22 = dht.DHT22( machine.Pin(23) )

# Use GPIO22=SCL, GPIO21=SDA
i2c_bus = 0 # use bus 0 or 1
i2c = machine.I2C( i2c_bus, freq=400000,
    scl=machine.Pin(22), sda=machine.Pin(21) )

# use I2C address = 0x3f
lcd = LCD(i2c, 0x3f)
lcd.clear() # clear display
lcd.goto_line( 0 ) # goto the first line
lcd.print('MicroPython...')
lcd.goto_line( 1 ) # goto the second line
lcd.print('DHT2 + LCD I2C')

try:
    saved_time = time.ticks_ms()
    state = 0
    while True:
        now = time.ticks_ms()
        if time.ticks_diff(now,saved_time) < 2000:
            continue
        saved_time = now
        if state == 0:
            try:
                dht22.measure()
            except OSError:
                print('DHT22 error')
                break
            state = 1
        else:
            t = dht22.temperature()
            h = dht22.humidity()
            lcd.clear()
            lcd.goto_line( 0 )
            lcd.print('T: {:.1f} deg.C'.format(t) )
            lcd.goto_line( 1 )
            lcd.print('H: {:.1f} %'.format(h) )
            state = 0
            
except KeyboardInterrupt:
    pass
finally:
    print('Done')

