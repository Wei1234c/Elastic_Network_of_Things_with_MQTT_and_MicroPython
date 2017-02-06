import gc
import micropython

gc.collect()
micropython.mem_info()

print('-----------------------------')
print('Initial free: {} allocated: {}'.format(gc.mem_free(), gc.mem_alloc()))


def func():
    a = bytearray(5000)
    
gc.collect()
print('Func definition: {} allocated: {}'.format(gc.mem_free(), gc.mem_alloc()))

func()

print('Func run free: {} allocated: {}'.format(gc.mem_free(), gc.mem_alloc()))

gc.collect()
print('Garbage collect free: {} allocated: {}'.format(gc.mem_free(), gc.mem_alloc()))
print('-----------------------------')

micropython.mem_info(1)


def clean_memory():
    print('[Memory - free: {} allocated: {}]'.format(gc.mem_free(), gc.mem_alloc()))
    gc.collect()
    
    
# import gc
# import micropython

# print('-----------------------------')
# gc.collect()
# free_before, loc_before = gc.mem_free(), gc.mem_alloc()
# print('Before free: {} allocated: {}'.format(free_before, loc_before))

# status = {'Datatransceiver ready': False,'Is connected': False, 'Stop': False}
# s = status.get('Datatransceiver ready')

# gc.collect()
# free_after, loc_after = gc.mem_free(), gc.mem_alloc()
# print('After free: {} allocated: {}'.format(free_after, loc_after))
# print('Diff: {}'.format(free_after - free_before, loc_after - loc_before))    

# print('-----------------------------')
# gc.collect()
# free_before, loc_before = gc.mem_free(), gc.mem_alloc()
# print('Before free: {} allocated: {}'.format(free_before, loc_before))

# status = {'Datatransceiver ready': False,'Is connected': False, 'Stop': False}
# s = status['Datatransceiver ready')

# gc.collect()
# free_after, loc_after = gc.mem_free(), gc.mem_alloc()
# print('After free: {} allocated: {}'.format(free_after, loc_after))
# print('Diff: {}'.format(free_after - free_before, loc_after - loc_before))    
