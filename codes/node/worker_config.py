# coding: utf-8

import config


if config.IS_MICROPYTHON:
    import machine
    unique_id = str(machine.unique_id())
    unique_id = unique_id.replace('\\', '_')    
    for c in ['b\'', '_x', ' ', '_', '\'', '(', ')', '#', '|']:
        unique_id = unique_id.replace(c, '')
    WORKER_NAME = 'NodeMCU_' + unique_id
    
    # WORKER_NAME = 'n_Lambda'
    # WORKER_NAME = 'n_Alpha'    
    # WORKER_NAME = 'n_Beta'
    
    
else:
    WORKER_NAME = 'Client_366'
