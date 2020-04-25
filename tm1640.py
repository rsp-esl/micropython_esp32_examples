# file: tm1640.py
# date: 2020-04-24

import machine
from machine import Pin
import utime as time
from micropython import const

class TM1640_LED_Matrix():
    # list of three commands of TM1640
    _CMD1   = const(0x40) # 0x40 data command
    _CMD2   = const(0xC0) # 0xC0 address command
    _CMD3   = const(0x80) # 0x80 display control command
    _DSP_ON = const(0x08) # 0x08 display on (bit mask)

    def __init__(self, sck, dio ):
        self._sck = sck
        self._dio = dio
        self._brightness = 3 # value range: 0..7
        self._disp_on = _DSP_ON
        self._vertical_invert = True
        self._sck(1)
        self._dio(1)
        
    def _send_dio(self, b):
        self._dio(b)
        time.sleep_us(10)
        
    def _send_sck(self, b):
        self._sck(b)
        time.sleep_us(10)
        
    def _start(self): # send start condition
        self._send_dio(0)
        self._send_sck(0)
        
    def _stop(self):  # send stop condition
        self._send_dio(0)
        self._send_sck(1)
        self._send_dio(1)
        
    def _write_byte(self, data, reverse=False):
        for i in range(8):
            if reverse:
                self._send_dio( (data >> (7-i)) & 1 )
            else:
                self._send_dio( (data >> i) & 1 )
            self._send_sck(1)
            self._send_sck(0)
            
    def _cmd_data(self):  # send CMD1
        self._start()
        self._write_byte( _CMD1 )
        self._stop()

    def _disp_ctrl(self): # send CMD3
        self._start()
        data = _CMD3 | self._disp_on | self._brightness 
        self._write_byte( data )
        self._stop()
    
    def on(self):    # turn on display 
        self._disp_on = _DSP_ON
        self._disp_ctrl()
        
    def off(self):   # turn off display
        self._disp_on = 0
        self._disp_ctrl()
        
    def clear(self): # clear display
        self.write( 16*[0] )
    
    def vertical_invert(self, b):
        self._vertical_invert = b

    def brightness(self,value=7): # set brightness level
        # brightness 0 =  1/16th pulse width
        # brightness 7 = 14/16th pulse width
        if 0 <= value <= 7:
            self._brightness = value
        self._cmd_data()
        self._disp_ctrl()
    
    def write(self, data, pos=0): # write display data
        if isinstance(data,int):
            data = [data]
        self._cmd_data()
        self._start()
        self._write_byte( _CMD2 | pos )
        for b in data:
            self._write_byte(b, self._vertical_invert)
        self._stop()
        self._disp_ctrl()

