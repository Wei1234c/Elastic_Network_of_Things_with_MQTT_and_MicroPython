# coding: utf-8

import config


if config.IS_MICROPYTHON:
    import machine
    import ubinascii
    unique_id = ubinascii.hexlify(machine.unique_id()).decode() 
    WORKER_NAME = 'NodeMCU_' + unique_id
    
    # WORKER_NAME = 'n_Lambda'
    # WORKER_NAME = 'n_Alpha'    
    # WORKER_NAME = 'n_Beta'    
    
else:
    WORKER_NAME = 'Client_366'
