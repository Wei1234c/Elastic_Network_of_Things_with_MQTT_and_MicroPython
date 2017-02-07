
# Network of Things test

Start a Mosquitto container first. For example:
- Use `codes\_demo\1_start_broker.sh` to start a Mosquitto container on Raspberry Pi.
- Config files are in `mqtt_config\mqtt`.
- set `allow_anonymous true` in `mqtt_config\mqtt\config\mosquitto.conf` to allow anonymous client.

## Getting Started
What this notebook does:  
- Using a client on PC
- List connected nodes
- Send messages to remote nodes:
 - Return results (read GPIOs)via RPC mechanism.
 - Write data to remote nodes (write GPIOs).
 - Execute arbitrary code on remote nodes.


```python
import os
import sys
import time
 
sys.path.append(os.path.abspath(os.path.join(os.path.pardir, 'codes', 'client')))
sys.path.append(os.path.abspath(os.path.join(os.path.pardir, 'codes', 'node')))
sys.path.append(os.path.abspath(os.path.join(os.path.pardir, 'codes', 'shared')))
sys.path.append(os.path.abspath(os.path.join(os.path.pardir, 'codes', 'micropython')))
 
import client
from collections import OrderedDict
```

### Start client


```python
the_client = client.Client()
the_client.start()

while not the_client.status['Is connected']:            
    time.sleep(1)
    print('Node not ready yet.')
```

    My name is Client_366
    
    Sending 277 bytes
    Message:
    OrderedDict([('command', 'set connection name'), ('correlation_id', '2017-02-07 15:02:17.079900'), ('kwargs', {'name': 'Client_366'}), ('message_id', '2017-02-07 15:02:17.079900'), ('message_type', 'command'), ('need_result', True), ('receiver', 'Hub'), ('reply_to', 'Client_366'), ('sender', 'Client_366')])
    
    
    [Connected: ('192.168.0.114', 1883)]
    [Listen to messages]
    Node not ready yet.
    

### Prepare messages


```python
# messages _____________________________________________
messages = OrderedDict()

messages['read_GPIOs'] = {'message_type': 'command',
                          'command': 'read GPIOs',
                          'kwargs': {'pins': [5, 12, 13, 14, 15, 16]},
                          'need_result': True}

messages['blink_led'] = {'message_type': 'command',
                         'command': 'blink led',
                         'kwargs': {'times': 3, 'forever': False, 'on_seconds': 0.1, 'off_seconds': 0.1}}
```


```python
# messages['write_GPIOs'] = {'message_type': 'command',
                           # 'command': 'write GPIOs',
                           # 'kwargs': {'pins_and_values': [(2, 0), (2, 1), (2, 0),]}} 

# messages['test eval'] = {'message_type': 'eval',
                         # 'to_evaluate': '2+3',
                         # 'need_result': True}                                   

# messages['test exec'] = {'message_type': 'exec',
                         # 'to_exec': 'print("Testing exec !")'}

# with open('script_to_deploy.py') as f:
    # script = f.read()        
# messages['test upload script'] = {'message_type': 'script', 
                                  # 'script': script} 
```

### List connected nodes


```python
the_client.node.worker.roll_call()
time.sleep(2)
remote_nodes = sorted(the_client.node.worker.contacts.keys())

print('\n[____________ Connected nodes ____________]\n')
print('\nConnected nodes:\n{}\n'.format(remote_nodes))
```

    
    Sending 249 bytes
    Message:
    OrderedDict([('correlation_id', '2017-02-07 15:02:29.200900'), ('function', 'check_in'), ('kwargs', {'caller': 'Client_366'}), ('message_id', '2017-02-07 15:02:29.200900'), ('message_type', 'function'), ('receiver', 'Hub'), ('reply_to', 'Client_366'), ('sender', 'Client_366')])
    
    
    Data received: 249 bytes
    Message:
    OrderedDict([('correlation_id', '2017-02-07 15:02:29.200900'), ('function', 'check_in'), ('kwargs', {'caller': 'Client_366'}), ('message_id', '2017-02-07 15:02:29.200900'), ('message_type', 'function'), ('receiver', 'Hub'), ('reply_to', 'Client_366'), ('sender', 'Client_366')])
    
    
    Sending 172 bytes
    
    Data received: 190 bytes
    Message:
    OrderedDict([('function', 'register_contact'), ('kwargs', {'name': 'NodeMCU_f1d30800', 'contact_id': 'NodeMCU_f1d30800'}), ('message_type', 'function'), ('receiver', 'Client_366'), ('sender', 'NodeMCU_f1d30800')])
    
    
    Data received: 178 bytes
    Message:
    OrderedDict([('function', 'register_contact'), ('kwargs', {'name': 'NodeMCU_8a00', 'contact_id': 'NodeMCU_8a00'}), ('message_type', 'function'), ('receiver', 'Client_366'), ('sender', 'NodeMCU_8a00')])
    
    
    Data received: 190 bytes
    Message:
    OrderedDict([('function', 'register_contact'), ('kwargs', {'name': 'NodeMCU_d1e0a200', 'contact_id': 'NodeMCU_d1e0a200'}), ('message_type', 'function'), ('receiver', 'Client_366'), ('sender', 'NodeMCU_d1e0a200')])
    
    
    Data received: 187 bytes
    Message:
    OrderedDict([('function', 'register_contact'), ('kwargs', {'name': 'NodeMCU_1dsc000', 'contact_id': 'NodeMCU_1dsc000'}), ('message_type', 'function'), ('receiver', 'Client_366'), ('sender', 'NodeMCU_1dsc000')])
    
    
    Data received: 190 bytes
    Message:
    OrderedDict([('function', 'register_contact'), ('kwargs', {'name': 'NodeMCU_a1a5c000', 'contact_id': 'NodeMCU_a1a5c000'}), ('message_type', 'function'), ('receiver', 'Client_366'), ('sender', 'NodeMCU_a1a5c000')])
    
    
    Data received: 184 bytes
    Message:
    OrderedDict([('function', 'register_contact'), ('kwargs', {'name': 'NodeMCU_edca00', 'contact_id': 'NodeMCU_edca00'}), ('message_type', 'function'), ('receiver', 'Client_366'), ('sender', 'NodeMCU_edca00')])
    
    
    Data received: 172 bytes
    Message:
    OrderedDict([('function', 'register_contact'), ('kwargs', {'name': 'Client_366', 'contact_id': 'Client_366'}), ('message_type', 'function'), ('receiver', 'Client_366'), ('sender', 'Client_366')])
    
    
    [____________ Connected nodes ____________]
    
    
    Connected nodes:
    ['Client_366', 'NodeMCU_1dsc000', 'NodeMCU_8a00', 'NodeMCU_a1a5c000', 'NodeMCU_d1e0a200', 'NodeMCU_edca00', 'NodeMCU_f1d30800']
    
    

### Read one GPIO pin


```python
for remote_node in remote_nodes:
    _, result = the_client.request(remote_node, messages['read_GPIOs']) 
    print('\nGPIO status for {}: {}\n'.format(remote_node, result.get()))
```

    
    Sending 286 bytes
    Message:
    OrderedDict([('command', 'read GPIOs'), ('correlation_id', '2017-02-07 15:02:38.741900'), ('kwargs', {'pins': [5, 12, 13, 14, 15, 16]}), ('message_id', '2017-02-07 15:02:38.741900'), ('message_type', 'command'), ('need_result', True), ('receiver', 'Client_366'), ('reply_to', 'Client_366'), ('sender', 'Client_366')])
    
    
    Data received: 286 bytes
    Message:
    OrderedDict([('command', 'read GPIOs'), ('correlation_id', '2017-02-07 15:02:38.741900'), ('kwargs', {'pins': [5, 12, 13, 14, 15, 16]}), ('message_id', '2017-02-07 15:02:38.741900'), ('message_type', 'command'), ('need_result', True), ('receiver', 'Client_366'), ('reply_to', 'Client_366'), ('sender', 'Client_366')])
    
    
    Processed result:
    OrderedDict([('correlation_id', '2017-02-07 15:02:38.741900'), ('message_id', '2017-02-07 15:02:39.678900'), ('message_type', 'result'), ('receiver', 'Client_366'), ('reply_to', 'Client_366'), ('result', 'Not applicable.'), ('sender', 'Client_366')])
    
    
    Sending 223 bytes
    Message:
    OrderedDict([('correlation_id', '2017-02-07 15:02:38.741900'), ('message_id', '2017-02-07 15:02:39.678900'), ('message_type', 'result'), ('receiver', 'Client_366'), ('reply_to', 'Client_366'), ('result', 'Not applicable.'), ('sender', 'Client_366')])
    
    
    Data received: 223 bytes
    Message:
    OrderedDict([('correlation_id', '2017-02-07 15:02:38.741900'), ('message_id', '2017-02-07 15:02:39.678900'), ('message_type', 'result'), ('receiver', 'Client_366'), ('reply_to', 'Client_366'), ('result', 'Not applicable.'), ('sender', 'Client_366')])
    
    
    GPIO status for Client_366: Not applicable.
    
    
    Sending 291 bytes
    Message:
    OrderedDict([('command', 'read GPIOs'), ('correlation_id', '2017-02-07 15:02:40.711900'), ('kwargs', {'pins': [5, 12, 13, 14, 15, 16]}), ('message_id', '2017-02-07 15:02:40.711900'), ('message_type', 'command'), ('need_result', True), ('receiver', 'NodeMCU_1dsc000'), ('reply_to', 'Client_366'), ('sender', 'Client_366')])
    
    
    Data received: 248 bytes
    Message:
    OrderedDict([('correlation_id', '2017-02-07 15:02:40.711900'), ('message_id', '99527'), ('message_type', 'result'), ('receiver', 'Client_366'), ('reply_to', 'NodeMCU_1dsc000'), ('result', [[5, 0], [12, 1], [13, 1], [14, 1], [15, 0], [16, 0]]), ('sender', 'NodeMCU_1dsc000')])
    
    GPIO status for NodeMCU_1dsc000: [[5, 0], [12, 1], [13, 1], [14, 1], [15, 0], [16, 0]]
    
    
    Sending 288 bytes
    
    Message:
    OrderedDict([('command', 'read GPIOs'), ('correlation_id', '2017-02-07 15:02:41.966900'), ('kwargs', {'pins': [5, 12, 13, 14, 15, 16]}), ('message_id', '2017-02-07 15:02:41.966900'), ('message_type', 'command'), ('need_result', True), ('receiver', 'NodeMCU_8a00'), ('reply_to', 'Client_366'), ('sender', 'Client_366')])
    
    
    Data received: 242 bytes
    Message:
    OrderedDict([('correlation_id', '2017-02-07 15:02:41.966900'), ('message_id', '87412'), ('message_type', 'result'), ('receiver', 'Client_366'), ('reply_to', 'NodeMCU_8a00'), ('result', [[5, 1], [12, 1], [13, 1], [14, 1], [15, 0], [16, 1]]), ('sender', 'NodeMCU_8a00')])
    
    
    GPIO status for NodeMCU_8a00: [[5, 1], [12, 1], [13, 1], [14, 1], [15, 0], [16, 1]]
    
    
    Sending 292 bytes
    Message:
    OrderedDict([('command', 'read GPIOs'), ('correlation_id', '2017-02-07 15:02:42.734900'), ('kwargs', {'pins': [5, 12, 13, 14, 15, 16]}), ('message_id', '2017-02-07 15:02:42.734900'), ('message_type', 'command'), ('need_result', True), ('receiver', 'NodeMCU_a1a5c000'), ('reply_to', 'Client_366'), ('sender', 'Client_366')])
    
    
    Data received: 251 bytes
    GPIO status for NodeMCU_a1a5c000: [[5, 0], [12, 1], [13, 1], [14, 1], [15, 0], [16, 0]]
    
    
    Message:
    OrderedDict([('correlation_id', '2017-02-07 15:02:42.734900'), ('message_id', '101118'), ('message_type', 'result'), ('receiver', 'Client_366'), ('reply_to', 'NodeMCU_a1a5c000'), ('result', [[5, 0], [12, 1], [13, 1], [14, 1], [15, 0], [16, 0]]), ('sender', 'NodeMCU_a1a5c000')])
    
    
    Sending 292 bytes
    Message:
    OrderedDict([('command', 'read GPIOs'), ('correlation_id', '2017-02-07 15:02:43.664900'), ('kwargs', {'pins': [5, 12, 13, 14, 15, 16]}), ('message_id', '2017-02-07 15:02:43.664900'), ('message_type', 'command'), ('need_result', True), ('receiver', 'NodeMCU_d1e0a200'), ('reply_to', 'Client_366'), ('sender', 'Client_366')])
    
    
    Data received: 250 bytes
    
    GPIO status for NodeMCU_d1e0a200: [[5, 1], [12, 1], [13, 1], [14, 1], [15, 0], [16, 1]]
    Message:
    OrderedDict([('correlation_id', '2017-02-07 15:02:43.664900'), ('message_id', '89198'), ('message_type', 'result'), ('receiver', 'Client_366'), ('reply_to', 'NodeMCU_d1e0a200'), ('result', [[5, 1], [12, 1], [13, 1], [14, 1], [15, 0], [16, 1]]), ('sender', 'NodeMCU_d1e0a200')])
    
    
    
    Sending 290 bytes
    Message:
    OrderedDict([('command', 'read GPIOs'), ('correlation_id', '2017-02-07 15:02:44.696900'), ('kwargs', {'pins': [5, 12, 13, 14, 15, 16]}), ('message_id', '2017-02-07 15:02:44.696900'), ('message_type', 'command'), ('need_result', True), ('receiver', 'NodeMCU_edca00'), ('reply_to', 'Client_366'), ('sender', 'Client_366')])
    
    
    Data received: 246 bytes
    Message:
    OrderedDict([('correlation_id', '2017-02-07 15:02:44.696900'), ('message_id', '60224'), ('message_type', 'result'), ('receiver', 'Client_366'), ('reply_to', 'NodeMCU_edca00'), ('result', [[5, 0], [12, 1], [13, 1], [14, 1], [15, 0], [16, 0]]), ('sender', 'NodeMCU_edca00')])
    
    
    GPIO status for NodeMCU_edca00: [[5, 0], [12, 1], [13, 1], [14, 1], [15, 0], [16, 0]]
    
    
    Sending 292 bytes
    Message:
    OrderedDict([('command', 'read GPIOs'), ('correlation_id', '2017-02-07 15:02:45.704900'), ('kwargs', {'pins': [5, 12, 13, 14, 15, 16]}), ('message_id', '2017-02-07 15:02:45.704900'), ('message_type', 'command'), ('need_result', True), ('receiver', 'NodeMCU_f1d30800'), ('reply_to', 'Client_366'), ('sender', 'Client_366')])
    
    
    Data received: 251 bytes
    Message:
    OrderedDict([('correlation_id', '2017-02-07 15:02:45.704900'), ('message_id', '104128'), ('message_type', 'result'), ('receiver', 'Client_366'), ('reply_to', 'NodeMCU_f1d30800'), ('result', [[5, 1], [12, 1], [13, 1], [14, 1], [15, 0], [16, 1]]), ('sender', 'NodeMCU_f1d30800')])
    
    
    GPIO status for NodeMCU_f1d30800: [[5, 1], [12, 1], [13, 1], [14, 1], [15, 0], [16, 1]]
    
    

### Blink each node
[YouTube video clip](https://youtu.be/I_s-no_0L24)


```python
for remote_node in remote_nodes:
    the_client.request(remote_node, messages['blink_led']) 
```

    
    Sending 300 bytes
    Message:
    OrderedDict([('command', 'blink led'), ('correlation_id', '2017-02-07 14:56:44.975900'), ('kwargs', {'on_seconds': 0.1, 'off_seconds': 0.1, 'forever': False, 'times': 3}), ('message_id', '2017-02-07 14:56:44.975900'), ('message_type', 'command'), ('receiver', 'Client_366'), ('reply_to', 'Client_366'), ('sender', 'Client_366')])
    
    
    Sending 304 bytes
    Message:
    OrderedDict([('command', 'blink led'), ('correlation_id', '2017-02-07 14:56:45.133900'), ('kwargs', {'on_seconds': 0.1, 'off_seconds': 0.1, 'forever': False, 'times': 3}), ('message_id', '2017-02-07 14:56:45.133900'), ('message_type', 'command'), ('receiver', 'NodeMCU_edca00'), ('reply_to', 'Client_366'), ('sender', 'Client_366')])
    
    
    Data received: 300 bytes
    Message:
    OrderedDict([('command', 'blink led'), ('correlation_id', '2017-02-07 14:56:44.975900'), ('kwargs', {'on_seconds': 0.1, 'off_seconds': 0.1, 'forever': False, 'times': 3}), ('message_id', '2017-02-07 14:56:44.975900'), ('message_type', 'command'), ('receiver', 'Client_366'), ('reply_to', 'Client_366'), ('sender', 'Client_366')])
    
    
    Data received: 245 bytes
    Message:
    OrderedDict([('command', 'set connection name'), ('correlation_id', '7277'), ('kwargs', {'name': 'NodeMCU_edca00'}), ('message_id', '7277'), ('message_type', 'command'), ('need_result', True), ('receiver', 'Hub'), ('reply_to', 'NodeMCU_edca00'), ('sender', 'NodeMCU_edca00')])
    
    
    Data received: 251 bytes
    Message:
    OrderedDict([('command', 'set connection name'), ('correlation_id', '8969'), ('kwargs', {'name': 'NodeMCU_f1d30800'}), ('message_id', '8969'), ('message_type', 'command'), ('need_result', True), ('receiver', 'Hub'), ('reply_to', 'NodeMCU_f1d30800'), ('sender', 'NodeMCU_f1d30800')])
    
    
    Data received: 250 bytes
    Message:
    OrderedDict([('command', 'set connection name'), ('correlation_id', '11244'), ('kwargs', {'name': 'NodeMCU_1dsc000'}), ('message_id', '11244'), ('message_type', 'command'), ('need_result', True), ('receiver', 'Hub'), ('reply_to', 'NodeMCU_1dsc000'), ('sender', 'NodeMCU_1dsc000')])
    
    
    Data received: 251 bytes
    Message:
    OrderedDict([('command', 'set connection name'), ('correlation_id', '6970'), ('kwargs', {'name': 'NodeMCU_f1d30800'}), ('message_id', '6970'), ('message_type', 'command'), ('need_result', True), ('receiver', 'Hub'), ('reply_to', 'NodeMCU_f1d30800'), ('sender', 'NodeMCU_f1d30800')])
    
    
    Data received: 248 bytes
    Message:
    OrderedDict([('command', 'set connection name'), ('correlation_id', '8981'), ('kwargs', {'name': 'NodeMCU_1dsc000'}), ('message_id', '8981'), ('message_type', 'command'), ('need_result', True), ('receiver', 'Hub'), ('reply_to', 'NodeMCU_1dsc000'), ('sender', 'NodeMCU_1dsc000')])
    
    
    Data received: 245 bytes
    Message:
    OrderedDict([('command', 'set connection name'), ('correlation_id', '9251'), ('kwargs', {'name': 'NodeMCU_edca00'}), ('message_id', '9251'), ('message_type', 'command'), ('need_result', True), ('receiver', 'Hub'), ('reply_to', 'NodeMCU_edca00'), ('sender', 'NodeMCU_edca00')])
    
    
    Data received: 251 bytes
    Message:
    OrderedDict([('command', 'set connection name'), ('correlation_id', '9503'), ('kwargs', {'name': 'NodeMCU_a1a5c000'}), ('message_id', '9503'), ('message_type', 'command'), ('need_result', True), ('receiver', 'Hub'), ('reply_to', 'NodeMCU_a1a5c000'), ('sender', 'NodeMCU_a1a5c000')])
    
    
    Data received: 241 bytes
    Message:
    OrderedDict([('command', 'set connection name'), ('correlation_id', '19274'), ('kwargs', {'name': 'NodeMCU_8a00'}), ('message_id', '19274'), ('message_type', 'command'), ('need_result', True), ('receiver', 'Hub'), ('reply_to', 'NodeMCU_8a00'), ('sender', 'NodeMCU_8a00')])
    
    
    Data received: 253 bytes
    Message:
    OrderedDict([('command', 'set connection name'), ('correlation_id', '20240'), ('kwargs', {'name': 'NodeMCU_d1e0a200'}), ('message_id', '20240'), ('message_type', 'command'), ('need_result', True), ('receiver', 'Hub'), ('reply_to', 'NodeMCU_d1e0a200'), ('sender', 'NodeMCU_d1e0a200')])
    
    

### Send out messages and get asynchonous results


```python
print('\n[______________ Sending messages ______________]\n')

results = []

# send out the messages
for message in messages.values():
    for remote_node in remote_nodes:
        if remote_node != the_client.node.worker.name:
            time.sleep(0.1)  # PyCharm needs this delay.
            formatted_message, asynch_result = the_client.request(remote_node, message)
            results.append((formatted_message, asynch_result))
```

    
    [______________ Sending messages ______________]
    
    
    Sending 291 bytes
    Message:
    OrderedDict([('command', 'read GPIOs'), ('correlation_id', '2017-02-07 15:03:08.566900'), ('kwargs', {'pins': [5, 12, 13, 14, 15, 16]}), ('message_id', '2017-02-07 15:03:08.566900'), ('message_type', 'command'), ('need_result', True), ('receiver', 'NodeMCU_1dsc000'), ('reply_to', 'Client_366'), ('sender', 'Client_366')])
    
    
    Sending 288 bytes
    Message:
    OrderedDict([('command', 'read GPIOs'), ('correlation_id', '2017-02-07 15:03:08.890900'), ('kwargs', {'pins': [5, 12, 13, 14, 15, 16]}), ('message_id', '2017-02-07 15:03:08.890900'), ('message_type', 'command'), ('need_result', True), ('receiver', 'NodeMCU_8a00'), ('reply_to', 'Client_366'), ('sender', 'Client_366')])
    
    
    Data received: 249 bytes
    Message:
    OrderedDict([('correlation_id', '2017-02-07 15:03:08.566900'), ('message_id', '126958'), ('message_type', 'result'), ('receiver', 'Client_366'), ('reply_to', 'NodeMCU_1dsc000'), ('result', [[5, 0], [12, 1], [13, 1], [14, 1], [15, 0], [16, 0]]), ('sender', 'NodeMCU_1dsc000')])
    
    
    Sending 292 bytes
    Message:
    OrderedDict([('command', 'read GPIOs'), ('correlation_id', '2017-02-07 15:03:09.268900'), ('kwargs', {'pins': [5, 12, 13, 14, 15, 16]}), ('message_id', '2017-02-07 15:03:09.268900'), ('message_type', 'command'), ('need_result', True), ('receiver', 'NodeMCU_a1a5c000'), ('reply_to', 'Client_366'), ('sender', 'Client_366')])
    
    
    Data received: 243 bytes
    Message:
    OrderedDict([('correlation_id', '2017-02-07 15:03:08.890900'), ('message_id', '114344'), ('message_type', 'result'), ('receiver', 'Client_366'), ('reply_to', 'NodeMCU_8a00'), ('result', [[5, 1], [12, 1], [13, 1], [14, 1], [15, 0], [16, 1]]), ('sender', 'NodeMCU_8a00')])
    
    
    Sending 292 bytes
    Message:
    OrderedDict([('command', 'read GPIOs'), ('correlation_id', '2017-02-07 15:03:09.557900'), ('kwargs', {'pins': [5, 12, 13, 14, 15, 16]}), ('message_id', '2017-02-07 15:03:09.557900'), ('message_type', 'command'), ('need_result', True), ('receiver', 'NodeMCU_d1e0a200'), ('reply_to', 'Client_366'), ('sender', 'Client_366')])
    
    
    Sending 290 bytes
    Message:
    OrderedDict([('command', 'read GPIOs'), ('correlation_id', '2017-02-07 15:03:09.799900'), ('kwargs', {'pins': [5, 12, 13, 14, 15, 16]}), ('message_id', '2017-02-07 15:03:09.799900'), ('message_type', 'command'), ('need_result', True), ('receiver', 'NodeMCU_edca00'), ('reply_to', 'Client_366'), ('sender', 'Client_366')])
    
    
    Data received: 251 bytes
    Message:
    OrderedDict([('correlation_id', '2017-02-07 15:03:09.268900'), ('message_id', '127726'), ('message_type', 'result'), ('receiver', 'Client_366'), ('reply_to', 'NodeMCU_a1a5c000'), ('result', [[5, 0], [12, 1], [13, 1], [14, 1], [15, 0], [16, 0]]), ('sender', 'NodeMCU_a1a5c000')])
    
    
    Sending 292 bytes
    Message:
    OrderedDict([('command', 'read GPIOs'), ('correlation_id', '2017-02-07 15:03:10.158900'), ('kwargs', {'pins': [5, 12, 13, 14, 15, 16]}), ('message_id', '2017-02-07 15:03:10.158900'), ('message_type', 'command'), ('need_result', True), ('receiver', 'NodeMCU_f1d30800'), ('reply_to', 'Client_366'), ('sender', 'Client_366')])
    
    
    Data received: 251 bytes
    Message:
    OrderedDict([('correlation_id', '2017-02-07 15:03:09.557900'), ('message_id', '115046'), ('message_type', 'result'), ('receiver', 'Client_366'), ('reply_to', 'NodeMCU_d1e0a200'), ('result', [[5, 1], [12, 1], [13, 1], [14, 1], [15, 0], [16, 1]]), ('sender', 'NodeMCU_d1e0a200')])
    
    
    Sending 305 bytes
    Message:
    OrderedDict([('command', 'blink led'), ('correlation_id', '2017-02-07 15:03:10.424900'), ('kwargs', {'on_seconds': 0.1, 'off_seconds': 0.1, 'forever': False, 'times': 3}), ('message_id', '2017-02-07 15:03:10.424900'), ('message_type', 'command'), ('receiver', 'NodeMCU_1dsc000'), ('reply_to', 'Client_366'), ('sender', 'Client_366')])
    
    
    Data received: 246 bytes
    Message:
    OrderedDict([('correlation_id', '2017-02-07 15:03:09.799900'), ('message_id', '85339'), ('message_type', 'result'), ('receiver', 'Client_366'), ('reply_to', 'NodeMCU_edca00'), ('result', [[5, 0], [12, 1], [13, 1], [14, 1], [15, 0], [16, 0]]), ('sender', 'NodeMCU_edca00')])
    
    
    Sending 302 bytes
    Message:
    OrderedDict([('command', 'blink led'), ('correlation_id', '2017-02-07 15:03:10.821900'), ('kwargs', {'on_seconds': 0.1, 'off_seconds': 0.1, 'forever': False, 'times': 3}), ('message_id', '2017-02-07 15:03:10.821900'), ('message_type', 'command'), ('receiver', 'NodeMCU_8a00'), ('reply_to', 'Client_366'), ('sender', 'Client_366')])
    
    
    Data received: 251 bytes
    Message:
    OrderedDict([('correlation_id', '2017-02-07 15:03:10.158900'), ('message_id', '128531'), ('message_type', 'result'), ('receiver', 'Client_366'), ('reply_to', 'NodeMCU_f1d30800'), ('result', [[5, 1], [12, 1], [13, 1], [14, 1], [15, 0], [16, 1]]), ('sender', 'NodeMCU_f1d30800')])
    
    
    Sending 306 bytes
    Message:
    OrderedDict([('command', 'blink led'), ('correlation_id', '2017-02-07 15:03:11.123900'), ('kwargs', {'on_seconds': 0.1, 'off_seconds': 0.1, 'forever': False, 'times': 3}), ('message_id', '2017-02-07 15:03:11.123900'), ('message_type', 'command'), ('receiver', 'NodeMCU_a1a5c000'), ('reply_to', 'Client_366'), ('sender', 'Client_366')])
    
    
    Sending 306 bytes
    Message:
    OrderedDict([('command', 'blink led'), ('correlation_id', '2017-02-07 15:03:11.438900'), ('kwargs', {'on_seconds': 0.1, 'off_seconds': 0.1, 'forever': False, 'times': 3}), ('message_id', '2017-02-07 15:03:11.438900'), ('message_type', 'command'), ('receiver', 'NodeMCU_d1e0a200'), ('reply_to', 'Client_366'), ('sender', 'Client_366')])
    
    
    Sending 304 bytes
    Message:
    OrderedDict([('command', 'blink led'), ('correlation_id', '2017-02-07 15:03:11.762900'), ('kwargs', {'on_seconds': 0.1, 'off_seconds': 0.1, 'forever': False, 'times': 3}), ('message_id', '2017-02-07 15:03:11.762900'), ('message_type', 'command'), ('receiver', 'NodeMCU_edca00'), ('reply_to', 'Client_366'), ('sender', 'Client_366')])
    
    
    Sending 306 bytes
    Message:
    OrderedDict([('command', 'blink led'), ('correlation_id', '2017-02-07 15:03:12.056900'), ('kwargs', {'on_seconds': 0.1, 'off_seconds': 0.1, 'forever': False, 'times': 3}), ('message_id', '2017-02-07 15:03:12.056900'), ('message_type', 'command'), ('receiver', 'NodeMCU_f1d30800'), ('reply_to', 'Client_366'), ('sender', 'Client_366')])
    
    

### Actually get the results


```python
# collect and print results        
print('\n[_________ Wait few seconds for reply _________]\n')
for (message, result) in results:
    try:
        if message.get('need_result'):
            print('\n[Result for request]:\n___Request___:\n{0}\n___Result____:\n{1}\n'.format(message,
                                                                                               result.get() if result else None))
    except Exception as e:
        print('\n[{}]\nMessage:\n{}'.format(e, message))
        
# Wait a while
time.sleep(3)        
```

    
    [_________ Wait few seconds for reply _________]
    
    
    [Result for request]:
    ___Request___:
    {'message_id': '2017-02-07 15:03:08.566900', 'need_result': True, 'command': 'read GPIOs', 'kwargs': {'pins': [5, 12, 13, 14, 15, 16]}, 'receiver': 'NodeMCU_1dsc000', 'message_type': 'command', 'reply_to': 'Client_366', 'correlation_id': '2017-02-07 15:03:08.566900', 'sender': 'Client_366'}
    ___Result____:
    [[5, 0], [12, 1], [13, 1], [14, 1], [15, 0], [16, 0]]
    
    
    [Result for request]:
    ___Request___:
    {'message_id': '2017-02-07 15:03:08.890900', 'need_result': True, 'command': 'read GPIOs', 'kwargs': {'pins': [5, 12, 13, 14, 15, 16]}, 'receiver': 'NodeMCU_8a00', 'message_type': 'command', 'reply_to': 'Client_366', 'correlation_id': '2017-02-07 15:03:08.890900', 'sender': 'Client_366'}
    ___Result____:
    [[5, 1], [12, 1], [13, 1], [14, 1], [15, 0], [16, 1]]
    
    
    [Result for request]:
    ___Request___:
    {'message_id': '2017-02-07 15:03:09.268900', 'need_result': True, 'command': 'read GPIOs', 'kwargs': {'pins': [5, 12, 13, 14, 15, 16]}, 'receiver': 'NodeMCU_a1a5c000', 'message_type': 'command', 'reply_to': 'Client_366', 'correlation_id': '2017-02-07 15:03:09.268900', 'sender': 'Client_366'}
    ___Result____:
    [[5, 0], [12, 1], [13, 1], [14, 1], [15, 0], [16, 0]]
    
    
    [Result for request]:
    ___Request___:
    {'message_id': '2017-02-07 15:03:09.557900', 'need_result': True, 'command': 'read GPIOs', 'kwargs': {'pins': [5, 12, 13, 14, 15, 16]}, 'receiver': 'NodeMCU_d1e0a200', 'message_type': 'command', 'reply_to': 'Client_366', 'correlation_id': '2017-02-07 15:03:09.557900', 'sender': 'Client_366'}
    ___Result____:
    [[5, 1], [12, 1], [13, 1], [14, 1], [15, 0], [16, 1]]
    
    
    [Result for request]:
    ___Request___:
    {'message_id': '2017-02-07 15:03:09.799900', 'need_result': True, 'command': 'read GPIOs', 'kwargs': {'pins': [5, 12, 13, 14, 15, 16]}, 'receiver': 'NodeMCU_edca00', 'message_type': 'command', 'reply_to': 'Client_366', 'correlation_id': '2017-02-07 15:03:09.799900', 'sender': 'Client_366'}
    ___Result____:
    [[5, 0], [12, 1], [13, 1], [14, 1], [15, 0], [16, 0]]
    
    
    [Result for request]:
    ___Request___:
    {'message_id': '2017-02-07 15:03:10.158900', 'need_result': True, 'command': 'read GPIOs', 'kwargs': {'pins': [5, 12, 13, 14, 15, 16]}, 'receiver': 'NodeMCU_f1d30800', 'message_type': 'command', 'reply_to': 'Client_366', 'correlation_id': '2017-02-07 15:03:10.158900', 'sender': 'Client_366'}
    ___Result____:
    [[5, 1], [12, 1], [13, 1], [14, 1], [15, 0], [16, 1]]
    
    

### Stop the demo


```python
# Stopping
the_client.stop()
the_client = None
print('\n[________________ Demo stopped ________________]\n')
```

    [Closed: ('192.168.0.114', 1883)]
    [________________ Demo stopped ________________]
    
    
    


```python

```
