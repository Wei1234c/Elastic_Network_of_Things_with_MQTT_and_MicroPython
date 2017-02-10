# MQTT websocket client:
# http://www.hivemq.com/demos/websocket-client/


import json
import datetime


def get_configuration():
    
    host = '192.168.0.114'    
    mqtt_websocket_port = 9001    
    group_name = 'u_python'    
    broker_name = 'Hub'    
    sender = 'Client'    
    broadcast_topic = '/'.join([group_name, broker_name])    
    mqtt_username = 'pi'    
    mqtt_password = 'raspberry'
    
    
    
    configuration = {}    
    
    configuration['broker'] = {'Host': host,
                               'Port': mqtt_websocket_port}
                               
    configuration['group_name'] = group_name
    
    configuration['broadcast topic'] = broadcast_topic
    
    configuration['client'] = {'name': sender,
                               'ClientID': '/'.join([group_name, sender]), 
                               'Username': mqtt_username,
                               'Password': mqtt_password}
                                   
    messages = {}
    
    messages["read_GPIOs"] = {"message": {"receiver": broker_name,
                                          "message_type": "command",
                                          "command": "read GPIOs",
                                          "kwargs": {"pins": [5, 12, 13, 14, 15, 16]},
                                          "need_result": True}}
                                          
    messages["blink_led"] = {"message": {"receiver": broker_name,
                                         "message_type": "command",
                                         "command": "blink led",
                                         "kwargs": {"times": 3,
                                                    "forever": False, 
                                                    "on_seconds": 0.1, 
                                                    "off_seconds": 0.1}}}

    messages["write_GPIOs"] = {"message": {"receiver": broker_name,
                                           "message_type": "command",
                                           "command": "write GPIOs",
                                           "kwargs": {"pins_and_values": [(2, 0), (2, 1), (2, 0),]}}}

    messages["test eval"] = {"message": {"receiver": broker_name,
                                         "message_type": "eval", 
                                         "to_evaluate": "2+3",
                                         "need_result": True}}

    messages["test exec"] = {"message": {"receiver": broker_name,
                                         "message_type": "exec",
                                         "to_exec": "print('Testing exec !')"}}
                        
    messages["roll call"] = {"message": {"receiver": broker_name,
                                         "message_type": "function",
                                         "function": "check_in",
                                         "kwargs": {"caller": sender}}} 

    configuration['messages'] = messages
    
    return configuration
    
    
def get_message(config, message):
    time_stamp = str(datetime.datetime.now())
    
    message = config['messages'][message]['message']
    message['sender'] = config['client']['name']
    message['message_id'] = time_stamp
    message['correlation_id'] = time_stamp
    
    topic = '/'.join([config['group_name'], message['receiver']])
    
    return json.dumps({'topic': topic, 'message': message}, sort_keys = True, indent = 4)


def list_messages():
    config = get_configuration()
    messages = sorted(config['messages'].items())
    for k, v in messages:
        print('[{}]\n{}\n'.format(k, get_message(config, k)))
        
    
    
def main():
    list_messages()
    

if __name__ == '__main__':
    main()
