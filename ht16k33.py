# file: ht16k33.py
# date: 2020-05-02

DIGITS = [ # font characters (3x8 pixels) for digits 0-9
    [0x7f,0x41,0x7f], # 0
    [0x41,0x7f,0x01], # 1
    [0x4f,0x49,0x79], # 2
    [0x49,0x49,0x7f], # 3
    [0x78,0x08,0x7f], # 4
    [0x79,0x49,0x4f], # 5
    [0x7f,0x49,0x4f], # 6
    [0x40,0x4f,0x70], # 7
    [0x7f,0x49,0x7f], # 8
    [0x79,0x49,0x7f]  # 9
]

class LED16X8():
    DISP_ADDR      = 0x80
    BRIGHTNESS_ADDR= 0xE0 
    OSC_ADDR       = 0x20
    BLINK_OFF      = 0x00
    BLINK_2HZ      = 0x02
    BLINK_1HZ      = 0x04

    def __init__(self, i2c, addr=0x70, bufsize=32):
        self._i2c  = i2c
        self._addr = addr
        self._reg  = bytearray(1)
        self._buf  = bufsize*[0]
        self._buf_size = bufsize
        self._disp_buf = 16*[0]
        self._offset = 0
        self._disp_on = 0
        self._brightness = 0
        self._blink_rate = 0
        self.brightness( 7 )
        self.shutdown( False )
        self.blink( self.BLINK_OFF )
        self.display_on( True )
        
    def shutdown(self,value=True):
        self._osc_on = int(not value)
        self._reg[0] = self.OSC_ADDR | self._osc_on 
        self._i2c.writeto( self._addr, self._reg )
        
    def display_on(self,value=True):
        self._disp_on = int(value)
        flags = self._blink_rate | self._disp_on
        self._reg[0] = self.DISP_ADDR | flags
        self._i2c.writeto( self._addr, self._reg )
        
    def blink(self, rate):
        self._blink_rate = (rate & 0b110)
        flags = self._blink_rate | self._disp_on
        self._reg[0] = self.DISP_ADDR | flags
        
    def brightness(self,value):
        self._brightness = value & 0x0f
        flag = self._brightness
        self._reg[0] = self.BRIGHTNESS_ADDR | flag
        self._i2c.writeto( self._addr, self._reg )
        
    def clear(self):
        self._disp_buf = 16*[0]
        self._buf = self._buf_size*[0]
        self.show()
        
    def write(self,pos,value,reverse=True):
        if pos < self._buf_size:
            value = self._reverse(value)
            self._buf[pos] = value
        
    def show(self,offset=0):
        for i in range(16):
            if (i+offset) >= self._buf_size:
                break
            elif (i+offset) < 0:
                continue
            if i >= 8:
                _pos = 2*(i-8) + 1
            else:
                _pos = 2*i
            self._disp_buf[_pos] = self._buf[i+offset]
        data = bytes([0]+self._disp_buf)
        self._i2c.writeto( self._addr, data )
        
    @staticmethod
    def _reverse(b):
        x = 0
        for i in range(8):
            x = (x << 1) | ((b >> i) & 1)
        return x

