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
        self.host = ""
        self.server_port = 9998
        # TODO: Finish init process with necessary code
        self.run()
        self.messageReceiver = MessageReceiver(self,self.connection)
        self.messageReceiver.start()

    def run(self):
        # Initiate the connection to the server
        self.connection.connect((self.host, self.server_port))

        
    def disconnect(self):
        self.messageReceiver.send_disconnect()
        self.connection.close()
        quit()

    def receive_message(self, message):
        self.messageParser.parse(self.printer, message)

    def printer(self,time,sender,message_type,message):
        melding = ("\n[" +
                time +" : " + message_type + "] " +
                sender+ ": " + message + "\n>>> ")
        print melding

    def send_payload(self, data):
        if data == "getHistory":
            self.messageReceiver.getHistory()
        elif data == "getNames":
            self.messageReceiver.getNames()
        elif data == "getHelp":
            self.messageReceiver.getHelp()
        else:
            self.messageReceiver.sendMessage(data)

    def login(self, data):
        brukerNavn = self.messageParser.parse_login(data)
        self.messageReceiver.send_login(brukerNavn)


if __name__ == '__main__':
    """
    This is the main method and is executed when you type "python Client.py"
    in your terminal.

    No alterations are necessary
    """
    client = Client('localhost', 9998)
    print("What is your name?")
    client.login(raw_input(">>> "))
    while (True):
        inputen = raw_input(">>> ").lower()
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

