# coding: utf-8

import config_mqtt


class Data_transceiver:
        
    def __init__(self):
        self.buffer = b''

    
    def pack(self, data):
        if data:
            return b'' + config_mqtt.PACKAGE_START + data.encode() + config_mqtt.PACKAGE_END
        
        
    # http://dabeaz.blogspot.tw/2010/01/few-useful-bytearray-tricks.html        
    def unpack(self, data):        
        if data:
            self.buffer += data
            end_at = self.buffer.find(config_mqtt.PACKAGE_END)
            
            if end_at > -1:
                start_at = self.buffer.find(config_mqtt.PACKAGE_START)
                message = self.buffer[start_at + len(config_mqtt.PACKAGE_START): end_at]
                self.buffer = self.buffer[end_at + len(config_mqtt.PACKAGE_END):]
                return data, message.decode()
                
        return data, None
