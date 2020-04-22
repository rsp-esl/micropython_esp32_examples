# file: spi_loopback.py 
# Date: 2020-04-22 

from machine import Pin, SPI
import utime

SCK  = const(14)
MOSI = const(13)
MISO = const(12)

hspi = SPI(1, baudrate=10000000, polarity=0, phase=0, bits=8, firstbit=SPI.MSB,
    sck=Pin(SCK), mosi=Pin(MOSI), miso=Pin(MISO))

for i in range(256):
    rbuf = bytearray(5*[0]) # read buffer filled with zero
    wbuf = bytearray( [0xaa,0xbb,0xcc,0xdd, i] )
    hspi.write_readinto( wbuf, rbuf )
    for b in rbuf:
        print( hex(b), end=' ' )
    print('')

hspi.deinit() # turn off the SPI bus

