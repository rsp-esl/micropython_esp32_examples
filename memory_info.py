# file: memory_info.py 
# Date: 2020-04-22 

import gc

mem_usage = (gc.mem_alloc(), gc.mem_free())
print( 'Memory: free=%d, alloc=%d in bytes' % mem_usage )

gc.collect() # calls the garbage collector
print( '1) Free mem:', gc.mem_free() )
N = const(5000)
big_list  = [x for x in range(N)] # create a list of integers
print( '2) Free mem:', gc.mem_free() )
zero_list = N*[0] # an array of zeros (0s)
print( '3) Free mem:', gc.mem_free() )
big_list  = []
zero_list = []
gc.collect()  # calls the garbage collector
print( '4) Free mem:', gc.mem_free() )

