# file: dht22_sensor_reading.py 
# Date: 2020-04-22 

from machine import Pin
import utime as time
import dht

GPIO_NUM = const(23) # use GPIO-23
dht22 = dht.DHT22( Pin( GPIO_NUM ) ) # create a DHT22 object

for i in range(10): # repeat the sensor reading 10 times
    # start the measurement
    try:
        dht22.measure()
    except OSError:
        print('DHT22 error')
        break
    # read values from DHT22
    t,h = dht22.temperature(), dht22.humidity()
    print( u'DHT22 readings: {:.1f}°C, {:.1f} %RH'.format(t,h) )
    time.sleep_ms(2000)

