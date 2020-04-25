# file: lcd_pcf8574.py
# date: 2020-04-23

import machine
import utime as time
from micropython import const

class LCD():
    _RS = const(0x01) # PCF8574 Pin 0 (RS)
    _RW = const(0x02) # PCF8574 Pin 1 (RW)
    _CS = const(0x04) # PCF8574 Pin 2 (CS or EN)
    _BL = const(0x08) # PCF8574 Pin 3
    
    _CURSOR_BLINK         = const(0x01)
    _CURSOR_ON            = const(0x02)
    _DISP_ON              = const(0x04)
    
    CMD_CLEAR_DISP        = const(0x01)
    CMD_RETURN_HOME       = const(0x02)
    CMD_CSTRY_MODE_SET    = const(0x04)
    CMD_DISP_CTRL         = const(0x08)
    CMD_CURSOR_DISP_SHIFT = const(0x10)
    CMD_FUNC_SET          = const(0x20)
    CMD_SET_CGRAM_ADDR    = const(0x40)
    CMD_SET_DDRAM_ADDR    = const(0x80)
    
    def __init__(self, i2c, addr):
        self._i2c  = i2c
        self._addr = addr
        self._disp_mode = 0
        self.reset()
    def _pcf8574_write( self, data ):
        self._i2c.writeto( self._addr, bytearray(data) )
        
    def _write4bits( self, data ):
        data = data | _BL
        self._pcf8574_write( [data | _CS] )
        time.sleep_us(300)
        self._pcf8574_write( [data] )
        time.sleep_us(300)
        
    def write( self, data, cmd=True ):
        _h = data & 0xf0        # high nibble
        _l = (data << 4) & 0xf0 # low nibble
        _mode = 0 if cmd else _RS
        self._write4bits( _h | _mode )
        self._write4bits( _l | _mode )
        
    def reset( self ):
        self._write4bits( 0x03 << 4 )
        time.sleep_ms(5)
        self._write4bits( 0x03 << 4)
        time.sleep_us(150)
        self._write4bits( 0x03 << 4)
        self._write4bits( 0x02 << 4)
        # function set: 4-bit data lines, 2 text lines, 5x8 dots
        self.write( CMD_FUNC_SET | 0x08 )
        # display ctrl: display on, cursor off
        self._disp_mode = _DISP_ON 
        self.write( CMD_DISP_CTRL | self._disp_mode )
        # go home position (move cursor to the first line)
        self.write( CMD_RETURN_HOME )
        
    def clear(self):
        self.write( CMD_CLEAR_DISP )
        
    def return_home( self ):
        self.write( CMD_RETURN_HOME )
        
    def goto_line( self, line ):
        addr = (0 if line==0 else 0x40) 
        self.write( CMD_SET_DDRAM_ADDR | addr )
        
    def blink_cursor( self, blink=True ):
        if blink:
            self._disp_mode |= _CURSOR_BLINK
        else:
            self._disp_mode &= ~ _CURSOR_BLINK
        self.write( CMD_DISP_CTRL | self._disp_mode )
        
    def show_cursor( self, show=True ):
        if show:
            self._disp_mode |= _CURSOR_ON
        else:
            self._disp_mode &= ~ _CURSOR_ON
        self.write( CMD_DISP_CTRL | self._disp_mode )
        
    def write_data( self, data ):
        self.write( data, False )
        
    def write_cmd( self, cmd ):
        self.write( cmd, True )
        
    def print( self, text ):
        for ch in text:
            self.write_data( ord(ch) )

