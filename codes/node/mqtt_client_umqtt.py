# coding: utf-8

import time
import socket
import gc
gc.collect()
import simple as umqtt
import config


class Message_client:
    # Object control
    def __init__(self, server_ip, server_port):
        self.server_address = socket.getaddrinfo(server_ip, server_port)[-1][-1]

        self.mqtt_client = umqtt.MQTTClient(client_id = self.name,
                                            server = self.server_address[0], port = self.server_address[1],
                                            user = config.USERNAME, password = config.PASSWORD,
                                            keepalive=60,
                                            ssl=False, ssl_params={})
        self.addr = self.server_address
        self.parent = None
        self.message = None
        self.receive_cycles = 0

        self.status = {'Datatransceiver ready': False,
                       'Is connected': False,
                       'Stop': False}

        self.mqtt_client.set_callback(self.on_message)


    def __del__(self):
        self.parent = None

        
    def set_parent(self, parent=None):
        self.parent = parent

        
    def run(self):
        self.connect()

        
    def stop(self):
        self.status['Stop'] = True
        self.close()

        
    def stopped(self):
        return self.status['Stop']


    def connect(self):
        while True:
            if self.stopped(): break

            try:
                self.status['Datatransceiver ready'] = False
                self.status['Is connected'] = False
                self.message = None
                self.mqtt_client.connect(clean_session=True)
                self.status['Datatransceiver ready'] = True
                self.on_connect()

            except Exception as e:
                print(e)
                time.sleep(config.CLIENT_RETRY_TO_CONNECT_AFTER_SECONDS)


    def on_connect(self):
        self.subscribe(topic = '/'.join([config.GROUP_NAME, self.name]), qos = config.QOS_LEVEL)
        self.subscribe(topic = '/'.join([config.GROUP_NAME, config.SERVER_NAME]), qos=config.QOS_LEVEL)
        print('\n[Connected: {0}]'.format(self.server_address))
        self.status['Is connected'] = True
        self.mqtt_client.check_msg()
        self.receive()


    def subscribe(self, topic, qos = config.QOS_LEVEL):
        self.mqtt_client.subscribe(topic = topic, qos = qos)


    def on_message(self, topic, msg):
        # print('Message topic: {}, payload: {}'.format(topic, str(msg)))
        self.on_receive(msg)


    def close(self):
        self.mqtt_client.disconnect()
        self.on_close()

        
    def on_close(self):
        print('[Closed: {}]'.format(self.server_address))

        
    def receive(self):
        print('[Listen to messages]')

        while True:
            if self.stopped(): break

            try:
                self.mqtt_client.sock.settimeout(config.CLIENT_RECEIVE_TIME_OUT_SECONDS)
                res = self.mqtt_client.wait_msg()
                
            except Exception as e:
                # Connection reset.
                if config.IS_MICROPYTHON:
                    if str(e) == config.MICROPYTHON_MQTT_CONNECTION_RESET_ERROR_MESSAGE:
                        raise e                            
                elif isinstance(e, ConnectionResetError):
                    raise e
                
                # Receiving process timeout.
                if self.receive_cycles % config.PING_BROKER_TO_KEEP_ALIVE_EVERY_CLIENT_RECEIVE_CYCLES == 0:
                    self.mqtt_client.ping()
                    self.receive_cycles = 0
                    
                self.receive_cycles += 1
                self.process_messages()    
                
                
    def process_messages(self):
        pass
        
        
    def receive_one_cycle(self):
        try:
            self.mqtt_client.check_msg()
        except Exception as e:
            pass

            
    def on_receive(self, data):
        if data:
            self.message = data.decode()
            print('\nData received: {0} bytes'.format(len(data)))

            
    def send_message(self, receiver, message_string):
        print('\nSending {} bytes'.format(len(message_string)))
        topic = '/'.join([config.GROUP_NAME, receiver])
        self.mqtt_client.publish(topic = topic,
                                 msg = message_string.encode(),
                                 retain = False,
                                 qos = config.QOS_LEVEL)
        self.mqtt_client.check_msg()