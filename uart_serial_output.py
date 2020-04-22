# file: uart_serial_output.py 
# Date: 2020-04-22 

from machine import UART
import math

TX = const(2)  # use GPIO2  for TXD
RX = const(15) # use GPIO15 for RXD
uart = UART(1, tx=TX, rx=RX, baudrate=115200, timeout=1000)

N = const(512)
for i in range(N): # repeat N times
    x = 100*(math.sin(2*math.pi*i/N))
    uart.write('{}\n'.format( round(x)) )
print('Done')

