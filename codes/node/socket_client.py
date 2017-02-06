# coding: utf-8

import time
import socket
import config
import data_transceiver


class Message_client:
    # Object control
    def __init__(self, server_ip, server_port):
        self.parent = None
        self.socket = None
        self.message = None
        self.data_transceiver = None
        self.server_address = socket.getaddrinfo(server_ip, server_port)[-1][-1]        
        self.status = {'Datatransceiver ready': False, 
                       'Is connected': False,
                       'Stop': False}
 

    def __del__(self):
        self.parent = None
        
 
    def set_parent(self, parent = None):        
        self.parent = parent

                  
    def run(self):        
        self.connect()        
 
 
    def stop(self):
        self.status['Stop'] = True
        self.close()
        

    def stopped(self):
        return self.status['Stop']
        
        
    
    # Socket operations
    def connect(self):        
        while True: 
            if self.stopped(): break             
                
            try:
                self.status['Datatransceiver ready'] = False
                self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.data_transceiver = data_transceiver.Data_transceiver()
                self.status['Datatransceiver ready'] = True
                self.message = None
                self.status['Is connected'] = False
                self.socket.connect(self.server_address)
                self.on_connect()  
                
            except Exception as e:
                print(e)
                time.sleep(config.CLIENT_RETRY_TO_CONNECT_AFTER_SECONDS)
            
    
    def on_connect(self):
        print('\n[Connected: {0}]'.format(self.server_address))
        self.status['Is connected'] = True
        self.receive()

        
    def close(self):
        self.socket.close()
        self.on_close()
        

    def on_close(self):
        print('[Closed: {}]'.format(self.server_address))
        del self.socket
            
    
    def receive(self):
        print('[Listen to messages]')
        self.socket.settimeout(config.CLIENT_RECEIVE_TIME_OUT_SECONDS)
        
        while True:
            if self.stopped(): break    
                
            try: 
                data = None
                data = self.socket.recv(config.BUFFER_SIZE)
                if len(data) == 0:  # If Broker shut down, need this line to close socket
                    self.on_close()
                    break
                self.on_receive(data)
                
            except Exception as e:                
                # Connection reset.
                if config.IS_MICROPYTHON:
                    if str(e) == config.MICROPYTHON_SOCKET_CONNECTION_RESET_ERROR_MESSAGE:
                        raise e
                elif isinstance(e, ConnectionResetError):
                    raise e

                # Receiving process timeout.
                self.process_messages()

    
    def receive_one_cycle(self):
        try: 
            data = None
            data = self.socket.recv(config.BUFFER_SIZE)
            if len(data) == 0:  # If Broker shut down, need this line to close socket
                self.on_close()
            self.on_receive(data)
            
        except Exception as e:                
            pass
        

    def on_receive(self, data):
        if data:
            data, message_string = self.data_transceiver.unpack(data)
            self.message = message_string
            print('\nData received: {0} bytes'.format(len(data)))
  

    def send_message(self, message_string):        
        message_bytes = self.data_transceiver.pack(message_string)
        print('\nSending {} bytes'.format(len(message_bytes)))        
        self.socket.sendall(message_bytes)            