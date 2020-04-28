# file: max7219.py
# date: 2020-04-28

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

    def __init__( self, spi, cs ):
        self._spi = spi
        self._cs  = cs
        self.init()

    def init( self ):
        # decode mode: no decode for digits 0-7
        self.write( REG_DECODE_MODE, 0 )
        # set intensity: 0x7 = 15/32, 0xf = 31/32
        self.write( REG_INTENSITY, 0xf )
        # scan limit: display digits 0-7
        self.write( REG_SCAN_LIMIT, 7 )
        # display test: normal (no display test)
        self.write( REG_DISP_TEST, 0 ) 
        # shutdown: normal operation (no shutdown)
        self.write( REG_SHUTDOWN, 1 )

    def write( self, reg, data ):
        if isinstance(data, int):
            data = [data]
        n = len(data)
        buf = []
        for i in range(n):
            buf += [reg, data[i]]
        self._cs.value(0) 
        self._spi.write( bytearray(buf) )
        self._cs.value(1)

    def clear( self, n=1 ):
        for i in range(8):
            self.write( REG_DIGIT_BASE+i, n*[0] )
    
    def on( self ):
        self.write( REG_SHUTDOWN, 1 )

    def off( self ):
        self.write( REG_SHUTDOWN, 0 )

    def flashing( self, times, delay_ms=100 ):
        for i in range(times):
            self.write( REG_DISP_TEST, 1 )
            time.sleep_ms( delay_ms )
            self.write( REG_DISP_TEST, 0 )
            time.sleep_ms( delay_ms )

    def deinit( self ):
        self._spi.deinit()
        del self._spi


