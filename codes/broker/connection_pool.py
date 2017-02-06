# coding: utf-8


import json
import data_transceiver


class Connection_pool:

    def __init__(self):
        self.connections = {}
        self.data_transceivers = {}
        self.connections_by_name = {}
                
        
    def register_connection(self, address, socket):
        connection = {'address': address, 'name': str(address), 'socket': socket}  
        self.connections[str(address)] = connection       
        self.regenerate_connections_by_name()
        self.data_transceivers[socket] = data_transceiver.Data_transceiver()
        return connection
        
        
    def remove_connection(self, address):
        self.data_transceivers.pop(self.connections.get(str(address)).get('socket'))
        connection = self.connections.pop(str(address))       
        self.regenerate_connections_by_name()         
        return connection
        
        
    def set_connection_name(self, name):
        address = self.socket_being_read.getpeername()
        connection = self.connections.get(str(address))
        if connection:
            connection['name'] = name             
        # sync
        self.regenerate_connections_by_name() 
        print('\n[Connection renamed]\n')        
        self.print_connections()        
        return self.connections_by_name

        
    def rename_connections(self, names = {}):
        # rename
        for old_name, new_name in names.items():  
            address = self.connections_by_name.get(old_name)
            connection = self.connections.get(str(address))
            if connection:
                connection['name'] = new_name                
        # sync
        self.regenerate_connections_by_name() 
        print('\n[Connections renamed]\n')        
        self.print_connections()        
        return self.connections_by_name
        
    
    def list_connections_by_name(self):
        return self.connections_by_name 
        
        
    def get_connection_by_name(self, name):        
        address = self.connections_by_name.get(name)        
        return self.connections.get(str(address))
       

    def get_connection(self, address = None, name = None):
        return self.connections.get(str(address)) if address else self.get_connection_by_name(name)
        
        
    def regenerate_connections_by_name(self):
        self.connections_by_name = {}                
        for address, connection in self.connections.items():
            self.connections_by_name[connection.get('name')] = address
            
            
    def get_sockets_list(self):
        return [connection.get('socket') for connection in self.connections.values()]

        
    def print_connections(self):
        print('Connections count: {0}'.format(len(self.connections_by_name.items())))
        connections = dict(self.connections_by_name.items())
        connections_list = json.dumps(connections, sort_keys = True, indent = 4)
        print('Connections:\n{0}\n'.format(connections_list))
