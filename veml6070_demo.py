# File: veml6070_demo.py
# Date: 2020-05-07

from machine import Pin,I2C
import utime as time

ADDR_L = 0x38 # 7bit address of the VEML6070 (write CMD, read LSB)
ADDR_H = 0x39 # 7bit address of the VEML6070 (read MSB)

levels = [(0,'low'),
          (2241,'moderate'),
          (4483,'high'),
          (5977,'very high'),
          (8217,'extreme') ]

i2c = I2C(1, scl=Pin(22), sda=Pin(21) )

SD = 0    # shutdown (disabled)
IT = 0b11 # integration time = 4T
cmd = (IT << 2) | SD
# write command to VEML6070
i2c.writeto( ADDR_L, bytes([cmd]) )

refresh_time = 500

try:
    while True:
        time.sleep_ms( refresh_time )
        # read the MSB (high byte)
        msb = i2c.readfrom( ADDR_H, 1)[0]
        # read the LSB (low byte)
        lsb = i2c.readfrom( ADDR_L, 1)[0]
        value = (msb <<8) | lsb # 16-bit value (unsigned)
        uv_index = ''
        for level in levels:
            if value < level[0]:
                break
            uv_index = level[1]
        print( 'VEML6070: {} ({})'.format(value,uv_index) )
            
except KeyboardInterrupt:
    pass
finally:
    print('Done')

