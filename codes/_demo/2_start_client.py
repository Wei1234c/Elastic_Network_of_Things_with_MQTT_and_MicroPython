# coding: utf-8

import os
import sys
import time

sys.path.append(os.path.abspath(os.path.join(os.path.pardir, 'client')))
sys.path.append(os.path.abspath(os.path.join(os.path.pardir, 'node')))
sys.path.append(os.path.abspath(os.path.join(os.path.pardir, 'shared')))
sys.path.append(os.path.abspath(os.path.join(os.path.pardir, 'micropython')))

import client
from collections import OrderedDict


def main():
    try:
        # start and wait until client thread is ready
        the_client = client.Client()
        the_client.start()

        # messages _____________________________________________
        messages = OrderedDict()

        messages['read_GPIOs'] = {'message_type': 'command',
                                  'command': 'read GPIOs',
                                  'kwargs': {'pins': [5, 12, 13, 14, 15, 16]},
                                  'need_result': True}

        messages['blink_led'] = {'message_type': 'command',
                                 'command': 'blink led',
                                 'kwargs': {'times': 3, 'forever': False, 'on_seconds': 0.1, 'off_seconds': 0.1}}

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


        while not the_client.status['Is connected']:
            time.sleep(1)
            print('Node not ready yet.')

        # nodes _________________________________________________
        # for home-brew broker
        # message = {'message_type': 'command',
                   # 'command': 'list connections by name',
                   # 'need_result': True}
        # _, asynch_result = the_client.request('Hub', message)
        # remote_nodes = sorted(list(asynch_result.get().keys()))


        # for MQTT broker        
        # message = {'receiver': 'Hub',
                   # 'message_type': 'function',
                   # 'function': 'check_in',
                   # 'kwargs': {'caller': the_client.node.worker.name}}
        # the_client.request('Hub', message)
        
        the_client.node.worker.roll_call()
        time.sleep(2)
        remote_nodes = sorted(the_client.node.worker.contacts_by_name().keys())


        # remote_nodes = ['NodeMCU_8a00']
        # remote_nodes = ['NodeMCU_1dsc000', 'NodeMCU_8a00']

        print('\n[____________ Connected nodes ____________]\n')
        print('\nConnected nodes:\n{}\n'.format(remote_nodes))

        print('\n[______________ Sending messages ______________]\n')

        results = []

        # send out the messages
        for message in messages.values():
            for remote_node in remote_nodes:
                if remote_node != the_client.node.worker.name:
                    time.sleep(0.1)  # PyCharm needs this delay.
                    formatted_message, asynch_result = the_client.request(remote_node, message)
                    results.append((formatted_message, asynch_result))

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

        # Stopping
        the_client.stop()
        the_client = None
        print('\n[________________ Demo stopped ________________]\n')

    except KeyboardInterrupt:
        print("Ctrl C - Stopping.")
        the_client.stop()
        the_client = None
        sys.exit(1)


if __name__ == '__main__':
    main()
