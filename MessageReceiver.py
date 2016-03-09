# -*- coding: utf-8 -*-
from threading import Thread
import json


class MessageReceiver(Thread):
    """
    This is the message receiver class. The class inherits Thread, something that
    is necessary to make the MessageReceiver start a new thread, and it allows
    the chat client to both send and receive messages at the same time
    """

    def __init__(self, client, conn):
        """
        This method is executed when creating a new MessageReceiver object
        """

        # Flag to run thread as a deamon
        super(MessageReceiver, self).__init__()
        self.daemon = True
        self.myconnection = conn
        self.myclient = client

        # TODO: Finish initialization of MessageReceiver

    def run(self):
        recv_message = self.myconnection.recv(4096)
        self.myclient.receive_message(recv_message)

    def sendMessage(self,data):
        message_to_be_sent = json.dumps({"request": "msg","content":data})
        self.myconnection.send(message_to_be_sent)
            #Done!

    def getHistory(self):
        message_to_be_sent = json.dumps({"request":"history","content":None})
        self.myconnection.send(message_to_be_sent)

    def getNames(self):
        message_to_be_sent = json.dumps({"request":"logout","content":None})
        self.myconnection.send(message_to_be_sent)

    def getHelp(self):
        message_to_be_sent = json.dumps({"request":"help","content":None})
        self.myconnection.send(message_to_be_sent)

    def send_disconnect(self):
        message_to_be_sent = json.dumps({"request":"logout","content":None})
        self.myconnection.send(message_to_be_sent)


    def send_login(self,login):
        self.myconnection.send(login)
