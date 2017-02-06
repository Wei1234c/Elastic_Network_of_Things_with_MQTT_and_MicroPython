# coding: utf-8

import config
import socket_server
import datetime
import json
now = datetime.datetime.now


class Hub(socket_server.Socket_server): 
        
    # code book_______________________
    def set_default_code_book(self):
        code_book = {'set connection name': self.set_connection_name,
                     'list connections by name': self.list_connections_by_name}      
        self.set_code_book(code_book)
        

    def process_message(self, message):
        if message:
            # time_stamp            
            time_stamp = str(datetime.datetime.now())
            message['time_stamp'] = time_stamp
            
            if message.get('receiver') == config.SERVER_NAME:    # message is dedicated to Hub
                if message.get('message_type') == 'result':  # result replied to Hub
                    pass
                
                else:   # new request to Hub 
                    
                    # do whatever said in the message.   
                    message, message_string = self.do(message)
                    
                    try:
                        reply_message = self.format_message(message_id = time_stamp,
                                                            sender = config.SERVER_NAME,
                                                            receiver = message.get('sender'),
                                                            time_stamp = time_stamp,
                                                            message_type = 'result',
                                                            need_result = False, result = message.get('result'),
                                                            reply_to = config.SERVER_NAME,
                                                            correlation_id = message.get('correlation_id'))
                                                
                        print('\nProcessed result:\n{0}\n'.format(json.dumps(reply_message,
                                                                             sort_keys = True, indent = 4)))
                        
                        # return result
                        if message.get('need_result'):                    
                            self.send_message(reply_message)
                        
                    except Exception as e:
                        print(e)
          
            else:   # new message to forward
                self.send_message(message)  
        

    def send_message(self, message):
        if message:           
            address = self.connections_by_name.get(message.get('receiver'))
            
            try:
                socket = self.connections.get(str(address)).get('socket')
                if socket:
                    message_string = self.encode_message(**message)
                    message_bytes = self.data_transceivers[socket].pack(message_string)
                    print('\nMessage sent: {0} bytes\n{1}\n'.format(len(message_bytes), json.dumps(message,
                                                                                                   sort_keys = True,
                                                                                                   indent = 4)))
                    socket.sendall(message_bytes) 
            except Exception as e:
                print(e)
