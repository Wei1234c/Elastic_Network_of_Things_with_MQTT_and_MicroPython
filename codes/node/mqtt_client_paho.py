# coding: utf-8

import time
import socket
import paho.mqtt.client as mqtt
import config


class Message_client:
    # Object control
    def __init__(self, server_ip, server_port):
        self.mqtt_client = mqtt.Client(client_id = self.name)  # , clean_session = True, userdata=None, protocol=MQTTv311, transport="tcp")
        self.mqtt_client.username_pw_set(config.USERNAME, config.PASSWORD)
        self.mqtt_client.max_inflight_messages_set(config.MAX_INFLIGHT_MESSAGES)
        self.parent = None
        self.message = None
        self.server_address = socket.getaddrinfo(server_ip, server_port)[-1][-1]        
        self.status = {'Datatransceiver ready': False, 
                       'Is connected': False,
                       'Stop': False}
 
        self.mqtt_client.on_connect = self.on_connect_mqtt
        self.mqtt_client.on_disconnect = self.on_disconnect_mqtt
        # self.mqtt_client.on_publish = self.on_publish_mqtt
        # self.mqtt_client.on_subscribe = self.on_subscribe_mqtt
        # self.mqtt_client.on_unsubscribe = self.on_unsubscribe_mqtt
        self.mqtt_client.on_message = self.on_message_mqtt
 

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
        
        
    
    def connect(self):
        while True:
            if self.stopped(): break

            try:
                self.status['Datatransceiver ready'] = False
                self.status['Is connected'] = False
                self.message = None
                self.mqtt_client.connect(host=self.server_address[0],
                                         port=self.server_address[1],
                                         keepalive=config.KEEPALIVE)
                self.status['Datatransceiver ready'] = True
                self.on_connect()

            except Exception as e:
                print(e)
                time.sleep(config.CLIENT_RETRY_TO_CONNECT_AFTER_SECONDS)
            

    def on_connect_mqtt(self, client, userdata, flags, rc):
        # print("Connected with result code {}".format(str(rc)))
        # print('\n[Connected: {0}]'.format(self.server_address))
        self.mqtt_client.subscribe(topic = '/'.join([config.GROUP_NAME, self.name]), qos = config.QOS_LEVEL)
        self.mqtt_client.subscribe(topic='/'.join([config.GROUP_NAME, config.SERVER_NAME]), qos=config.QOS_LEVEL)


    def on_connect(self):
        print('\n[Connected: {0}]'.format(self.server_address))
        self.status['Is connected'] = True
        self.receive()
        
        
    def on_disconnect_mqtt(self, client, userdata, rc):
        # print("Disconnected with result code {}".format(str(rc)))
        self.on_close()
        

    # def on_publish_mqtt(self, client, userdata, mid):
        # print("On publish {}".format(mid))        
        

    # def on_subscribe_mqtt(self, client, userdata, mid, granted_qos):
        # print("On subscribe, mid:{}, granted_qos:{}".format(mid, granted_qos))        
        
            
    # def on_unsubscribe_mqtt(self, client, userdata, mid):
        # print("On unsubscribe {}".format(mid))        
        
            
    # The callback for when a PUBLISH message is received from the server.
    def on_message_mqtt(self, client, userdata, message):
        # print('Message topic: {}, payload: {}'.format(message.topic, str(message.payload)))
        self.on_receive(message.payload)
        

    # def on_log_mqtt(self, client, userdata, level, buf):
        # print("On log level: {}, buf: {}".format(level, buf))
            
            


        
    def close(self):
        self.mqtt_client.disconnect()
        

    def on_close(self):
        print('[Closed: {}]'.format(self.server_address))
            
            
    def receive(self):
        print('[Listen to messages]')
        # self.socket.settimeout(config.CLIENT_RECEIVE_TIME_OUT_SECONDS)
        
        while True:
            if self.stopped(): break    
                
            try:
                self.mqtt_client.loop(timeout = config.CLIENT_RECEIVE_TIME_OUT_SECONDS)
                self.process_messages()
            except Exception as e: 
                print(e)

    
    def receive_one_cycle(self):
        try:
            # self.mqtt_client.loop(timeout = config.CLIENT_RECEIVE_TIME_OUT_SECONDS)
            self.process_messages()
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
                                 payload = message_string.encode(),
                                 qos = config.QOS_LEVEL, retain = False)        