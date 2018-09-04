# coding: utf-8

import config_mqtt


if config_mqtt.IS_MICROPYTHON:
    import machine
    import ubinascii
    uuid = ubinascii.hexlify(machine.unique_id()).decode() 
    WORKER_NAME = 'NodeMCU_' + uuid
    
    # WORKER_NAME = 'n_Lambda'
    # WORKER_NAME = 'n_Alpha'    
    # WORKER_NAME = 'n_Beta'    
    
else:
    WORKER_NAME = 'Client_366'
