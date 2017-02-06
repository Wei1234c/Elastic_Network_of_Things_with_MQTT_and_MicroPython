# coding: utf-8

import os
import sys
import threading
 
sys.path.append(os.path.abspath(os.path.join(os.path.pardir, 'shared')))
sys.path.append(os.path.abspath(os.path.join(os.path.pardir, 'node')))

import node


class Client(threading.Thread):
    
    def __init__(self):        
        super().__init__(name = 'Client', daemon = True)
        self.node = node.Node()
        self.status = self.node.worker.status
        
        
    def _request(self, receiver, message):
        message['receiver'] = receiver
        return self.node.request(**message)
        
        
    def request(self, receiver, message):
        try:
            return self._request(receiver, message)
        except Exception as e:
            print(e)
        
        
    def run(self):
        self.node.run()
       
       
    def stop(self):
        self.node.stop()
