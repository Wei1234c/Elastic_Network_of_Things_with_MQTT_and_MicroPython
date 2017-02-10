# coding: utf-8

import gc
import config

if config.IS_MICROPYTHON:
    import mqtt_client_umqtt as message_client
else:
    import mqtt_client_paho as message_client

import queue_manager
import commander
import phonebook
import asynch_result
import worker_config


class Worker(message_client.Message_client,
             queue_manager.Queue_manager,
             commander.Commander,
             phonebook.Phonebook):
        
    # Object control
    def __init__(self, server_address, server_port):
        self.name = worker_config.WORKER_NAME
        super().__init__(server_address, server_port)
        queue_manager.Queue_manager.__init__(self)        
        commander.Commander.__init__(self)
        phonebook.Phonebook.__init__(self)
        print('My name is', self.name)
        
         
    # Socket operations 
    def on_connect(self):
        # set my name
        self.set_connection_name()
        super().on_connect()
        

    def rename(self, name):
        self.name = name
        self.set_connection_name()
        
        
    def set_connection_name(self):
        # set my name
        message = self.format_message(sender = self.name,
                                      receiver = config.SERVER_NAME,
                                      message_type = 'command', 
                                      command = 'set connection name',
                                      kwargs = {'name': self.name}, 
                                      need_result = True)
        self.request(message)


    def check_in(self, caller):
        message = self.format_message(sender = self.name,
                                      receiver = caller,
                                      message_type = 'function',
                                      function = 'register_contact',
                                      kwargs = {'contact_id': self.name, 'name': self.name})
        # self.request(message)
        # self.send_message(message)
        # self.append_request_message(message)
        super().send_message(caller, self.encode_message(**message))


    def on_receive(self, data):        
        super().on_receive(data)
        gc.collect()
        if self.message:
            try:
                self.message = self.decode_message(self.message)
                print('Message:\n{}\n'.format(self.get_OrderedDict(self.message)))
                self.append_received_message(self.message)
                self.process_messages()
            except Exception as e:
                print(e)
        
        
    def process_messages(self):
        gc.collect()
        if config.IS_MICROPYTHON:
            print('[Memory - free: {}   allocated: {}]'.format(gc.mem_free(), gc.mem_alloc()))
        
        time_stamp = str(self.now())
        
        # outgoing requested messages
        message = self.pop_request_message()
        if message: self.send_message(message = message)

        # incoming messages
        message = self.pop_received_message()
        if message: 
            
            # got result from somewhere else, no need to reply.
            if message.get('message_type') == 'result':
                pass
                
            else:
                # do whatever said in the message.   
                message, message_string = self.do(message)

                try:
                    if message and message.get('need_result'):
                        reply_message = self.format_message(message_id = time_stamp,
                                                            sender = self.name,
                                                            receiver = message.get('sender'),
                                                            message_type = 'result',
                                                            need_result = False, result = message.get('result'),
                                                            reply_to = self.name,
                                                            correlation_id = message.get('correlation_id'))
                        
                        print('\nProcessed result:\n{0}\n'.format(self.get_OrderedDict(reply_message)))
                        self.send_message(reply_message)
                    
                except Exception as e:
                    print(e, 'No result to return.')

        
    def request(self, message):
        time_stamp = str(self.now())
        message['message_id'] = time_stamp
        message['sender'] = self.name
        message['reply_to'] = self.name          
        message['result'] = None
        message['correlation_id'] = time_stamp
        message = self.format_message(**message)
        self.append_request_message(message)
        if self.status['Datatransceiver ready']: self.process_messages()
            
        async_result = None
        if message.get('need_result'):
            async_result = asynch_result.Asynch_result(message.get('correlation_id'),
                                                       self._requests_need_result,
                                                       self.receive_one_cycle)
        return message, async_result
       

    def send_message(self, message):
        message_string = self.encode_message(**message)
        super().send_message(message.get('receiver'), message_string)        
        print('Message:\n{}\n'.format(self.get_OrderedDict(message)))
