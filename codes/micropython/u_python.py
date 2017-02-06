# coding: utf-8

import machine
import hardware
    

def get_output_pin(pin_id, mode = machine.Pin.OUT, pull = None):
    return machine.Pin(pin_id, mode, pull)
    
    
def get_input_pin(pin_id, mode = machine.Pin.IN):
    return machine.Pin(pin_id, mode)


def read_GPIOs_pins(pins):
    status = sorted([(pin_id, get_input_pin(pin_id).value()) for pin_id in pins])
    return status

    
def write_GPIOs_pins(pins_and_values):
    for pin_id, value in pins_and_values:
        the_pin = get_output_pin(pin_id, mode = machine.Pin.OUT)
        the_pin.value(value)
    return read_GPIOs_pins(pins_and_values.keys())
