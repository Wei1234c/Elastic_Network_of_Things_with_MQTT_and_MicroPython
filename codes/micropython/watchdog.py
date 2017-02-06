# coding: utf-8

import machine

my_dog = None


def set_watchdog(the_dog = my_dog, wd_id = 0, timeout = 5000):
    the_dog = machine.WDT(wd_id, timeout)
    
    
def feet_the_dog(the_dog = my_dog, ):
    the_dog.feed()
