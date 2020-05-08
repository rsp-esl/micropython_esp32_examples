# file: ir_receiver.py
# date: 2020-05-08

from machine import Pin, Timer
import utime as time
from micropython import const

HEAD_INIT_MARK_MIN    = const(4000)
HEAD_INIT_SPACE_MIN   = const(4000)
HEAD_REPEAT_MARK_MIN  = const(HEAD_INIT_MARK_MIN)
HEAD_REPEAT_SPACE_MIN = const(HEAD_INIT_SPACE_MIN//2)
BIT_MARK_MIN   = const(400)
BIT_MARK_MAX   = const(700)
BIT0_SPACE_MIN = const(BIT_MARK_MIN)
BIT0_SPACE_MAX = const(BIT_MARK_MAX)
BIT1_SPACE_MIN = const(1500)
BIT1_SPACE_MAX = const(1800)
    
class IR_RECV():
    """This class implements an IR receiver/decoder for NEC protocol."""
    
    def __init__(self, pin, timer_id=-1,timeout=100):
        self._ts = 128*[0] # array for timestamp values (usec)
        self._saved_ts = 0
        self._index    = -1
        self._max_cnt  = 0
        self._timeout  = timeout
        self._pin = pin # IR input pin
        self._pin.init( mode=Pin.IN, pull=Pin.PULL_UP )
        trig_mode = (Pin.IRQ_FALLING | Pin.IRQ_RISING)
        self._pin.irq( trigger=trig_mode, handler=self._pin_cb )
        self._tim = Timer( timer_id ) # software timer
        self._codes = []
    
    def _decode(self):
        mark, space = self._ts[0], self._ts[1]
        if mark < HEAD_INIT_MARK_MIN:
            return
        if space > HEAD_INIT_SPACE_MIN: 
            # found start sequence
            bits = []
            for i in range(2,self._max_cnt,2):
                mark, space = self._ts[i], self._ts[i+1]
                if BIT_MARK_MIN < mark < BIT_MARK_MAX:
                    if BIT0_SPACE_MIN < space < BIT0_SPACE_MAX:
                        bits.append('0')
                    elif BIT1_SPACE_MIN < space < BIT1_SPACE_MAX:
                        bits.append('1')
                else: # error
                    return
            bin_str = ''.join(bits)
            try:
                if len(bin_str) > 0:
                    # only 32-bit value
                    code = (int(bin_str,2)) & 0xffffffff
                    hex_str = hex(code)[2:]
                    self._codes.append( hex_str )
            except Exception as ex:
                pass
        elif space > HEAD_REPEAT_SPACE_MIN:
            if self._max_cnt == 3:
                self._codes.append( '0' ) # repeat code   
        
    def _timer_cb(self, t):
        self._tim.init(callback=None)
        self._max_cnt = self._index
        self._index = -1
        if self._max_cnt > 1:
            self._decode() # decode bits
    
    def read(self):
        _codes = self._codes[:]
        self._codes = []
        return _codes
    
    def _pin_cb(self, p):
        # read current timestamp
        ts = time.ticks_us()
        if self._index == -1:
            # detected the first event (transition)
            # start timer in one-shot mode
            self._tim.init( period=self._timeout,
                            mode=Timer.ONE_SHOT,
                            callback=self._timer_cb )
        elif self._index < len(self._ts):
            t_width = time.ticks_diff(ts, self._saved_ts)
            self._ts[ self._index ] = t_width
        self._index += 1
        self._saved_ts = ts
       
    def deinit(self):
        self._pin.irq(handler=None)
        self._tim.deinit()

