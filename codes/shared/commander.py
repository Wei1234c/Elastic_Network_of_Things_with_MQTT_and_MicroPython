# coding: utf-8

import json
import config


if config.IS_MICROPYTHON:
    from ucollections import OrderedDict
else:
    from collections import OrderedDict


class Commander:

    def __init__(self):
        self.code_book = None
        self.set_default_code_book()
        self.switch = {'file': self.do_file,
                       'script': self.do_script,
                       'command': self.do_command,
                       'function': self.do_function,
                       'exec': self.do_exec,
                       'eval': self.do_eval}


    def set_code_book(self, code_book = {}):
        self.code_book = code_book


    def set_default_code_book(self):
        self.code_book = {}


    # https://docs.python.org/3.5/library/json.html
    def encode_message(self, **kwargs):
        try:
            return json.dumps(self.format_message(**kwargs))
        except Exception as e:
            print(e)


    def format_message(self,
                       sender, receiver, message_type,
                       message_id = None,
                       info = None,
                       time_stamp = None,
                       file = None,
                       script = None,
                       to_exec = None,
                       to_evaluate = None,
                       command = None,
                       function = None, kwargs = None,
                       need_result = False, result = None,
                       reply_to = None, correlation_id = None):

        message = {}
        if sender: message['sender'] = sender
        if receiver: message['receiver'] = receiver
        if message_type: message['message_type'] = message_type
        if message_id: message['message_id'] = message_id
        if info: message['info'] = info
        if time_stamp: message['time_stamp'] = time_stamp
        if file: message['file'] = file
        if script: message['script'] = script
        if to_exec: message['to_exec'] = to_exec
        if to_evaluate: message['to_evaluate'] = to_evaluate
        if command: message['command'] = command
        if function: message['function'] = function
        if kwargs: message['kwargs'] = kwargs
        if need_result: message['need_result'] = need_result
        if result: message['result'] = result
        if reply_to: message['reply_to'] = reply_to
        if correlation_id: message['correlation_id'] = correlation_id

        return message


    def get_OrderedDict(self, dictionary):
        return OrderedDict(sorted(dictionary.items()))


    def decode_message(self, message_string):
        if message_string:
            try:
                return json.loads(message_string)
            except Exception as e:
                print(e)


    def do(self, message):
        if message: return self.switch[message.get('message_type')](message)


    def do_file(self, message):
        filename = None
        if message.get('file'):
            kwargs = message.get('kwargs')
            if kwargs:
                filename = kwargs.get('filename')
            filename = filename if filename else 'uploaded_file.py'
            with open(filename, 'w') as f:
                f.write(message.get('file'))

        return None, None


    def do_script(self, message):
        if message.get('script'):
            with open('script.py', 'w') as f:
                f.write(message.get('script'))
            import script
            script.main()

        return None, None


    def do_exec(self, message):
        if message.get('to_exec'):
            exec(message.get('to_exec'))

        return None, None


    def do_eval(self, message):
        if message.get('to_evaluate'):
            result = eval(message.get('to_evaluate'))
            return self.process_result(message, result)

        return None, None


    def do_function(self, message):
        if message.get('function'):
            task = getattr(self, message.get('function'))
            return self.do_task(task, message)

        return None, None


    def do_command(self, message):
        if message.get('command'):
            task = self.code_book.get(message.get('command'))
            return self.do_task(task, message)

        return None, None


    def do_task(self, task, message):
        if task:
            try:
                kwargs = message.get('kwargs')
                result = task(**kwargs) if kwargs else task()
                return self.process_result(message, result)
            except Exception as e:
                print(e)

        return None, None


    def process_result(self, message, result):
        if message.get('need_result'):
            message['message_type'] = 'result'
            message['result'] = result
            return message, self.encode_message(**message)

        return None, None
