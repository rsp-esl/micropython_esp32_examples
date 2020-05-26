# File: max7219.py
# Date: 2020-05-26

from micropython import const 
from machine import Pin, SPI
import utime as time

class MAX7219():
    REG_DIGIT_BASE   = const(0x1)
    REG_DECODE_MODE  = const(0x9)
    REG_INTENSITY    = const(0xA)
    REG_SCAN_LIMIT   = const(0xB)
    REG_SHUTDOWN     = const(0xC)
    REG_DISP_TEST    = const(0xF)
    
    def __init__( self, spi, cs, n=1 ):
        self._spi = spi # spi bus
        self._cs  = cs  # cs pin
        self._n   = n   # number of blocks
        self.init()
        
    def init( self ):
        # decode mode: no decode for digits 0-7
        self.write( REG_DECODE_MODE, self._n*[0] )
        # set intensity: 0x7 = 15/32, 0xf = 31/32
        self.write( REG_INTENSITY, self._n*[0xf] )
        # scan limit: display digits 0-7
        self.write( REG_SCAN_LIMIT, self._n*[7] )
        # display test: normal (no display test)
        self.write( REG_DISP_TEST, self._n*[0] ) 
        # shutdown: normal operation (no shutdown)
        self.write( REG_SHUTDOWN, self._n*[1] )
        
    def write( self, reg, data ):
        if isinstance(data, int):
            data = [data]
        n = len(data)
        buf = []
        for i in range(n):
            buf += [reg, data[i]]
        self._cs.value(0) # assert CS pin 
        self._spi.write( bytearray(buf) ) # write SPI data
        self._cs.value(1) # deassert CS pin
        
    def clear( self ):
        for i in range(8):
            self.write( REG_DIGIT_BASE+i, self._n*[0] )
            
    def on( self ):
        self.write( REG_SHUTDOWN, self._n*[1] )
        
    def off( self ):
        self.write( REG_SHUTDOWN, self._n*[0] )
        
    def flashing( self, times, delay_ms=100 ):
        for i in range(times):
            self.write( REG_DISP_TEST, self._n*[1] )
            time.sleep_ms( delay_ms )
            self.write( REG_DISP_TEST, self._n*[0] )
            time.sleep_ms( delay_ms )
            
    def deinit( self ):
        self._spi.deinit()
