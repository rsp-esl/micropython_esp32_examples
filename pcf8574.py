# file: pcf8574.py
# date: 2020-05-05

from machine import Pin, I2C

ROT_LSHIFT = lambda x: ((x << 1) | (x >> 7)) & 0xff
ROT_RSHIFT = lambda x: ((x >> 1) | (x << 7)) & 0xff

class PCF8574():
    def __init__(self,i2c,addr,pin_irq=None):
        self._i2c = i2c
        self._addr = addr
        self._int  = pin_irq
        self._changes = 0
        # initial state: P0..P7 input direction
        self.write_byte( 0xff )
        if self._int != None:
            self._int.init(mode=Pin.IN, pull=Pin.PULL_UP)
            self._int.irq(handler=self._callback,
                          trigger=Pin.IRQ_FALLING)
    
    def _callback(self,p):
        self._changes += 1
    
    def set_callback(self,cb=None):
        if self._int != None:
            self._int.irq(handler=cb,
                          trigger=Pin.IRQ_FALLING)
    
    def write_byte(self, value):
        self._i2c.writeto( self._addr, bytes([value]) )
    
    def pin_changed(self):
        return (self._changes != 0)
    
    def read_byte(self):
        self._changes = 0
        value = self._i2c.readfrom(self._addr, 1)[0]
        return value
    
    def deinit(self):
        self.write_byte( 0xff )
        if self._int != None:
            self._int.irq(handler=None)

class PCF8574_BUTTONS(PCF8574):
    def __init__(self,i2c,addr,pin_irq=None):
        super().__init__(i2c,addr,pin_irq)
        self._saved_inputs = 0xff
    
    def button_clicked(self):
        inputs = self.read_byte()
        change = (inputs ^ self._saved_inputs) != 0
        self._saved_inputs = inputs
        results = []
        for i in range(8):
            state = change and (((inputs>>i)&1)==0)
            results.append(state)
        return results

class PCF8574_LED_BAR(PCF8574):
    def __init__(self,i2c,addr,init_value=0xff):
        super().__init__(i2c,addr)
        self._value = init_value
        self.update()
    
    def set_value(self,value):
        self._value = value
    
    def rotate_left(self):
        self._value = ROT_LSHIFT(self._value)
    
    def rotate_right(self):
        self._value = ROT_RSHIFT(self._value)
    
    def update(self):
        self.write_byte(self._value)

