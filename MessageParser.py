# -*- coding: utf-8 -*-
import json


class MessageParser():
    def __init__(self):

        self.possible_responses = {
            'error': self.parse_error,
            'info': self.parse_info,
            'message': self.parse_message,
            'history': self.parse_history,
            'login': self.parse_login
        }

    def parse(self,printer, payload):
        payload = json.loads(payload)
        
        if "request" in payload.keys():
            if payload['request'] in self.possible_responses:
                return self.possible_responses[payload['request']](printer, payload)
            else:
                pass
        else:
            if payload["response"] in self.possible_responses:
                return self.possible_responses[payload['response']](printer, payload)
            else:
                pass
      

    def parse_error(self, printer, payload):
        data = json.loads(payload)
        time = data['timestamp']
        sender = data['sender']
        message_type = "Error"
        message = data['content']
        printer(time,sender,message_type,message)
    
    def parse_info(self, printer, data):
        time = data['timestamp']
        sender = data['sender']
        message_type = "Info"
        message = data['content']
        printer(time,sender,message_type,message)

    def parse_message(self, printer, data):
        time = data['timestamp']
        sender = data['sender']
        message_type = "Message"
        message = data['content']
        printer(time,sender,message_type,message)

    def parse_history(self, printer, payload):
        message = payload["content"]
        time = payload['timestamp']
        sender = payload['sender']
        message_type = "History"
        printer(time, sender, message_type, "Here is a list of all previous messages")
        for objekt in message:
            data = json.loads(objekt)
            time = data["timestamp"]
            sender = data["sender"]
            message_type = "Message"
            message = data["content"]
            printer(time,sender,message_type,message)
    
    def parse_login(self, name):
        for letter in name:
            if not(letter.isalpha() or letter.isdigit()):
                raise ValueError("Your name can only contain a-z, A-Z, 0-9!!!")
        return name
