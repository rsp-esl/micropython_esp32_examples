# file: ir_receiver_demo-2.py
# date: 2020-05-08

from machine import Pin, Timer
import utime as time
import neopixel
from ir_receiver import IR_RECV

keys = {
    '0': 'REPEAT',
    'ffa25d': 'POWER',
    'ff629d': 'UP',
    'ffa857': 'DOWN',
    'ff22dd': 'LEFT',
    'ffc23d': 'RIGHT',
    'ffe01f': 'HOME',
    'ffe21d': 'BACK',
    'ff02fd': 'PLAY',
    'ff906f': 'TEXT',
    'ff6897': '0',
    'ff30cf': '1',
    'ff18e7': '2',
    'ff7a85': '3',
    'ff10ef': '4',
    'ff38c7': '5',
    'ff5aa5': '6',
    'ff42bd': '7',
    'ff4ab5': '8',
    'ff52ad': '9',
    'ff9867': '-',
    'ffb04f': '+', }

ir = IR_RECV( Pin(12), timeout=80 )
np = neopixel.NeoPixel(Pin(19), 1)
rgb = 3*[0]
color = 0
np[0] = tuple(rgb) # rgb color = (0,0,0)
np.write()

try:
    prev_key = None
    while True:
        codes = ir.read() # read IR code
        if len(codes) > 0 and codes[0] in keys:
            code = codes[0]
            print( code, keys[code] )
            if code != '0':
                prev_key = keys[code]
            key = prev_key 
            if key == 'UP':
                value = rgb[color]
                rgb[color] = min(value+8,255)
            elif key == 'DOWN':
                value = rgb[color]
                rgb[color] = max(value-8,0)
            elif key == 'HOME':
                rgb = 3*[0]
                color = 0
            elif key in ['0','1','2']:
                color = int(key)
            elif key == 'POWER':
                break
            np[0] = tuple(rgb)
            np.write()
        time.sleep_ms(100) 
except KeyboardInterrupt:
    pass
finally:
    ir.deinit()
    np[0] = (0,0,0)
    np.write()
    print('Done')

