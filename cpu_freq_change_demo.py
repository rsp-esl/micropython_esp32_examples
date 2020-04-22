# file: cpu_freq_change_demo.py 
# CPU Frequency Setting demo
# Date: 2020-04-22 

import machine
from micropython import const
import utime as time
import math
import gc

def test_func():
    # number of values 
    N = const(512) 
    # calculate a sine function with a float argument
    y = [math.sin(2*math.pi*i/N) for i in range(N)]

# read and save the current frequency in Hz
saved_freq = machine.freq()

# list of CPU frequencies to be used 
frequencies = [20, 40, 80, 160, 240]

# array used to keep execution times
exec_time_results = []

NUM_LOOPS = const(5)
for f in frequencies:
    machine.freq( f*1000000 )
    sum = 0
    for i in range(NUM_LOOPS):
       t1 = time.ticks_us()
       test_func()
       t2 = time.ticks_us()
       sum += ( t2-t1 )
       y = None
       gc.collect() # perform garbage collection
    exec_time_results.append( sum//(NUM_LOOPS*1000) )
    time.sleep_ms(10)

# show the results 
for p in list(zip(frequencies, exec_time_results)):
    print( '{:3} MHz -> exec time: {:4d} msec'.format(p[0],p[1]) )

# restore the CPU frequency 
machine.freq( saved_freq )

