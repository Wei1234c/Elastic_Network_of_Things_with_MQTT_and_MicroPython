# coding: utf-8

import config
       

class Phonebook:    
    
    def __init__(self):
        self.contacts = {}

        
    def roll_call(self):
        self.contacts = {}
        message = self.format_message(sender=self.name,
                                      receiver=config.SERVER_NAME,
                                      message_type='function',
                                      function='check_in',
                                      kwargs={'caller': self.name})
        self.request(message)


    def register_contact(self, contact_id, name = None):
        name = name if name else contact_id
        self.contacts[contact_id] = {'contact_id': contact_id, 'name': name}


    def remove_contact(self, contact_id):
        self.contacts.pop(contact_id)


    def set_contact_name(self, contact_id, name):
        contact = self.contacts.get(contact_id)
        if contact: contact['name'] = name


    def contacts_by_name(self):
        cons = {}
        for contact_id, contact in self.contacts.items():
            cons[contact.get('name')] = contact_id
        return cons
