# file: dac_adc_loopback.py 
# Date: 2020-04-22 

from machine import Pin, ADC, DAC
import utime as time

# Connect GPIO25 (DAC output) to GPIO34 (ADC input) !!!

ADC_GPIO = const(34) # use GPIO-34 for ADC input channel
adc = ADC(Pin(ADC_GPIO))   # create an ADC object
adc.atten(ADC.ATTN_11DB)   # set 11dB attenuation for input
adc.width(ADC.WIDTH_10BIT) # set 10 bit return values

# note: GPIO25 (Channel 2) and GPIO26 (Channel 1)
DAC_NUM = const(26)        # GPIO26 
dac = DAC( Pin(DAC_NUM) )  # 8-bit DAC

NUM_SAMPLES = const(8)
for value in range(255):
    dac.write( value )
    time.sleep_us(100)
    samples = []
    for j in range(NUM_SAMPLES):
        samples.append( adc.read() )
    # calcuate the average value from N samples
    value_avg = round(sum(samples)/NUM_SAMPLES)
    print( 'DAC:{:4d} -> ADC:{:5d}'.format(value, value_avg) )

