# file: ir_receiver_demo-1.py
# date: 2020-05-08

from machine import Pin
import utime as time
from ir_receiver import IR_RECV

ir = IR_RECV( Pin(12), timeout=80 )
try:
    while True:
        codes = ir.read()
        for code in codes:
            print("Code: '{}'".format(code) )
        time.sleep_ms(100) 
except KeyboardInterrupt:
    pass
finally:
    ir.deinit()
    print('Done')

