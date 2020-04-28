# file: max7219_demo.py
# date: 2020-04-28
from micropython import const
from machine import Pin, SPI
import utime as time
from max7219 import MAX7219

SCK  = const(14)
MOSI = const(13)
MISO = const(12)
CS   = const(27)

SPI(1).deinit()
spi = SPI(1, baudrate=8000000,
    polarity=0, phase=0, bits=8,
    firstbit=SPI.MSB, sck=Pin(SCK,Pin.OUT),
    mosi=Pin(MOSI,Pin.OUT), miso=Pin(MISO,Pin.IN))
cs = Pin(CS, Pin.OUT, value=1)

disp = MAX7219(spi,cs)
disp.clear()

heart = [
  0b00000000,
  0b01100110,
  0b11111111,
  0b11111111,
  0b01111110,
  0b00111100,
  0b00011000,
  0b00000000, ]

disp.on()
for i in range(8):
    disp.write( MAX7219.REG_DIGIT_BASE+i, heart[7-i] )
time.sleep(2.0)

# flashing 10 times 200 msec delay
disp.flashing(10,200) 
disp.off()
disp.deinit()
del disp
