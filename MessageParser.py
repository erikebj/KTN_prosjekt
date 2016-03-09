import json


class MessageParser():
    def __init__(self):

        self.possible_responses = {
            'error': self.parse_error,
            'info': self.parse_info,
            'message': self.parse_message,
            'history': self.parse_history
        }

    def parse(self, payload):
        payload = json.loads(payload)
 

        if payload['response'] in self.possible_responses:
            return self.possible_responses[payload['response']](payload)
        else:
            pass

    def parse_error(self, payload):
        data = json.loads(payload)
        time = data['timestamp']
        sender = data['sender']
        message_type = "Error"
        message = data['content']
        return (time,sender,message_type,message)
    
    def parse_info(self, payload):
        data = json.loads(payload)
        time = data['timestamp']
        sender = data['sender']
        message_type = "Info"
        message = data['content']
        return (time,sender,message_type,message)



    def parse_message(self, payload):
        data = json.loads(payload)
        time = data['timestamp']
        sender = data['sender']
        message_type = "Message"
        message = data['content']
        return (time,sender,message_type,message)

    def parse_history(self, payload):
        # We need a list of some sort here due to multiple objects arriving.
        #TODO Add some type of list
        data = json.loads(payload)
        time = data['timestamp']
        sender = data['sender']
        message_type = "History"
        message = data['content']
        return (time,sender,message_type,message)
    
    def parse_login(self, payload):
        data = json.loads(payload)
        name = data['content']
        for letter in name:
            if not(letter.isalpha() or letter.isdigit()):
                raise ValueError("Your name can only contain a-z, A-Z, 0-9!!!")
        return json.dumps(payload)
    # Include more methods for handling the different responses...
