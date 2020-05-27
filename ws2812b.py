# File: ws2812b.py
# Date: 2020-05-27

import esp32
import utime as time

class WS2812B:
    """An implementation of a WS2812B driver using ESP32-RMT"""
    
    BIT0 = [4,8] # T0H = 0.4us, T0L = 0.8us
    BIT1 = [8,4] # T1H = 0.8us, T1L = 0.4us
    
    def __init__(self, pin, n=1):
        self._n = n
        self._data = n*[(0,0,0)]
        self._rmt = esp32.RMT(0, pin=pin, clock_div=8)
    
    def __setitem__(self, index, val):
        if index < 0 or index >= self._n:
            raise IndexError('Index out of range')
        if isinstance( val, tuple ):
            self._data[index] = val
        elif isinstance( val, int):
            r = (val >> 16) & 0xff
            g = (val >> 8) & 0xff
            b = val & 0xff
            self._data[index] = (r,g,b)
        
    def _getitem(self, index):
        if 0 <= index and index < self._n:
            return self._data[index]
        else:
            return None
    
    def clear(self):
        self._data = self._n*[(0,0,0)]
        self.update()
    
    def shift_left(self, new_val=None):
        first = self._data.pop(0)
        self._data.append((0,0,0))
        if new_val is not None:
            self[self._n-1] = new_val
        else:
            self[self._n-1] = first
        return first
    
    def shift_right(self, new_val=None):
        last = self._data.pop(self._n-1)
        self._data.insert(0,(0,0,0))
        if new_val is not None:
            self[0] = new_val
        else:
            self[0] = last
        return last
    
    def update(self):
        bits = []
        for t in self._data:
            r,g,b = t
            v = (g << 16) | (r << 8) | b
            for i in range(23,-1,-1):
                if (v >> i) & 1:
                    bits += self.BIT1
                else:
                    bits += self.BIT0
        self._rmt.write_pulses(bits, start=1) 
        while not self._rmt.wait_done(): 
            pass
        
    def deinit(self):
        self._rmt.deinit()


