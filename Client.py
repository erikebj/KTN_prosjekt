# -*- coding: utf-8 -*-
import socket
import json
from MessageReceiver import MessageReceiver
from MessageParser import MessageParser

class Client:
    """
    This is the chat client class
    """
    def __init__(self, host, server_port):
        """
        This method is run when creating a new Client object
        """

        # Set up the socket connection to the server
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.messageParser = MessageParser()
        self.messageReceiver = MessageReceiver(self,self.connection)
        self.host = host
        self.server_port = server_port
        # TODO: Finish init process with necessary code
        self.run()

    def run(self):
        # Initiate the connection to the server
        self.connection.connect((self.host, self.server_port))

        
    def disconnect(self):
        self.messageReceiver.send_disconnect()
        self.connection.close()
        quit()

    def receive_message(self, message):                     # Recieving a message from the messagereciver, parses this
        self.printer(MessageParser.parse(message))        # message and then calls for a print.


    def printer(self,time,sender,message_type,message):     # Printing to the user
        print "<<<<<<<      >>>>>>>"
        print time +": " + sender + ": " + message_type
        print ": " + message

    def send_payload(self, data):
        if data == "getHistory":
            self.messageReceiver.getHistory()
        elif data == "getNames":
            self.messageReceiver.getNames()
        elif data == "getHelp":
            self.messageReceiver.getHelp()
        else:
            melding = data
            self.messageReceiver.sendMessage(melding)

    def login(self, data):
        melding = json.dumps({"request": "login", "content": data})
        inlogging = self.messageParser.parse(melding)
        self.messageReceiver.send_login(inlogging)           # Login sent to Reciever as a JSON object.
        
    # More methods may be needed!


if __name__ == '__main__':
    """
    This is the main method and is executed when you type "python Client.py"
    in your terminal.

    No alterations are necessary
    """
    client = Client('localhost', 9998)
    print("What is your name?")
    client.login(input(">>> "))
    while (True):
        inputen = input(">>> ").lower()
        if inputen == "logout":
            client.disconnect()
        elif inputen == "history":
            client.send_payload("getHistory")
        elif inputen == "names":
            client.send_payload("getNames")
        elif inputen == "help":
            client.send_payload("getHelp")
        else:
            client.send_payload(inputen)

