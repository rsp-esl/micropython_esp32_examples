# file: tm1638.py
# date: 2020-04-30

from micropython import const
from machine import Pin
from time import sleep_us, sleep_ms

DIGITS = bytearray(b'\x3F\x06\x5B\x4F\x66\x6D\x7D\x07\x7F\x6F')

class TM1638():
    _CMD1 = const(0x40)       # data command
    _CMD2 = const(0xC0)       # address command
    _CMD3 = const(0x80)       # display control command
    _KEY_READ = const(0x02)   # read key scan data flag for CMD1
    _DISP_ON  = const(0x08)   # display on flag for CMD3

    def __init__(self, stb, clk, dio, brightness=7):
        self._stb = stb
        self._clk = clk
        self._dio = dio
        self._brightness = brightness # 0..7
        self._disp_on    = _DISP_ON
        self._clk.init( Pin.OUT, value=1 )
        self._dio.init( Pin.OUT, value=0 )
        self._stb.init( Pin.OUT, value=1 )
        self.clear()

    def _write_byte(self, b):
        for i in range(8):
            self._clk(0)
            self._dio((b >> i) & 1) # LSB first
            self._clk(1)

    def _cmd1(self):
        self._stb(0) # start 
        # write mode, auto-increment addressing, normal mode
        self._write_byte(_CMD1)
        self._stb(1) # stop

    def _cmd2(self, data, addr=0):
        self._stb(0) # start
        # set address start, followed by one data byte 
        self._write_byte( _CMD2 | (addr & 0xf) )
        if isinstance(data,list):
            for b in data:
                self._write_byte( b )
                sleep_us(1)
        else:
            self._write_byte( data )
        self._stb(1) # stop

    def _cmd3(self):
        self._stb(0) # start
        # display command: display on, set brightness
        self._write_byte( _CMD3 | self._disp_on | self._brightness )
        self._stb(1) # stop

    def on(self):
        self._disp_on = _DISP_ON
        self._cmd3()

    def off(self):
        self._disp_on = 0
        self._cmd3()

    def brightness(self, val=7):
        self._brightness = val & 0b111
        self._cmd3()

    def clear(self):
        self.write( 16*[0], 0 )

    def write(self, data, addr=0):
        self._cmd1()
        self._cmd2( data, addr )
        self._cmd3()

    def led(self, pos, value):
        self._cmd1()
        self._cmd2( value, (pos << 1) | 1 )

    def segment(self, pos, value):
        self._cmd1()
        self._cmd2( value, (pos << 1) )
        
    def read_buttons(self):
        value = 0
        self._stb(0)
        self._write_byte( _CMD1 | _KEY_READ )
        self._dio.init( Pin.IN, Pin.PULL_UP )
        for j in range(4): # read 4 bytes
            temp = 0
            for i in range(4): # read nibble
                self._clk(0)
                if self._dio.value():
                    temp = 0x08
                self._clk(1)
            for i in range(4): # read nibble
                self._clk(0)
                if self._dio.value():
                    temp = 0x80
                self._clk(1)
            value = (value >> 1) | temp
        self._dio.init( Pin.OUT, 0 )
        self._stb(1)
        return value

