# file: adc_analog_input_reading.py 
# Date: 2020-04-22 

from machine import Pin, ADC
import utime as time
ADC_GPIO = const(34) # use GPIO-34 for ADC input channel
adc = ADC(Pin(ADC_GPIO),unit=1) # create an ADC object

adc.atten(ADC.ATTN_11DB)   # set 11dB attenuation for input
adc.width(ADC.WIDTH_12BIT) # set 12 bit return values

NUM_SAMPLES = const(8)
for i in range(20): # repeat 20 times
    samples = []
    for j in range(NUM_SAMPLES):
        samples.append( adc.read() )
    # calcuate the average value from N samples
    value_avg = round(sum(samples)/NUM_SAMPLES)
    print( 'ADC: {:4d}'.format(value_avg))
    time.sleep_ms(500)

