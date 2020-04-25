# file: lcd16x2_pcf8574_demo-2.py
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

# for 5x8 -> 8 bytes per char, each byte b4..b0
# up to 8 chars (8x8 or 64 bytes -> 6-bit CGRAM address)
# see: online tool https://omerk.github.io/lcdchargen/
thermo_symbol = [
0b00100,
0b01010,
0b01010,
0b01010,
0b01110,
0b11111,
0b11111,
0b01110
]

deg_symbol = [
0b00100,
0b01010,
0b00100,
0b00000,
0b00000,
0b00000,
0b00000,
0b00000]

humid_symbol = [
0b00100,
0b00100,
0b01010,
0b01010,
0b10001,
0b10001,
0b10011,
0b01110
]

# use I2C address = 0x3f
lcd = LCD(i2c, 0x3f)
lcd.clear() # clear display
lcd.goto_line( 0 ) # goto the first line
lcd.print('MicroPython...')
lcd.goto_line( 1 ) # goto the second line
lcd.print('DHT2 + LCD I2C')

lcd.write_cmd( lcd.CMD_SET_CGRAM_ADDR | 0 )
for symbol in [thermo_symbol, deg_symbol, humid_symbol]:
    for i in range(8):
        lcd.write_data( symbol[i] )

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
            lcd.print('    \x00 {:.1f}\x01C'.format(t) )
            lcd.goto_line( 1 )
            lcd.print('    \x02 {:.1f} %'.format(h) )
            state = 0
            
except KeyboardInterrupt:
    pass
finally:
    print('Done')

