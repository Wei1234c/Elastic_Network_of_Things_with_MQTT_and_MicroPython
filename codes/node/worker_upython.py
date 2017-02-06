# coding: utf-8


import time
import worker
import led
import u_python


class Worker(worker.Worker):
        
    # Object control
    def __init__(self, server_address, server_port):
        super().__init__(server_address, server_port)
        self.now = time.ticks_ms
        
        
    # code book_______________________
    def set_default_code_book(self):
        code_book = {'read GPIOs': self.read_GPIOs,
                     'write GPIOs': self.write_GPIOs,
                     'blink led': self.blink_led}      
        self.set_code_book(code_book)        
        
        
    def rename(self, name):
        self.name = name
        
        
    def read_GPIOs(self, pins):
        return u_python.read_GPIOs_pins(pins)
        

    def write_GPIOs(self, pins_and_values): 
        return u_python.write_GPIOs_pins(pins_and_values)
        
    
    def blink_led(self, times = 1, forever = False, on_seconds = 0.5, off_seconds = 0.5):
        led.blink_on_board_led(times = times, 
                               forever = forever,
                               on_seconds = on_seconds,
                               off_seconds = off_seconds)
