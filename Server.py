# -*- coding: utf-8 -*-
import SocketServer
import json
from time import gmtime, strftime

"""
Variables and functions that must be used by all the ClientHandler objects
must be written here (e.g. a dictionary for connected clients)
"""

Users = []
class ClientHandler(SocketServer.BaseRequestHandler):
    """
    This is the ClientHandler class. Everytime a new client connects to the
    server, a new ClientHandler object will be created. This class represents
    only connected clients, and not the server itself. If you want to write
    logic for the server, you must write it outside this class
    """
    name = None
    def handle(self):
        """
        This method handles the connection between a client and the server.
        """
        self.ip = self.client_address[0]
        self.port = self.client_address[1]
        self.connection = self.request

        self.responses = {
                "login": self.login,
                "logout": self.logout,
                "msg": self.msg,
                "names": self.names,
                "help": self.helper,
                "history": self.history
            }
        # Loop that listens for messages from the client
        while True:
            received_string = self.connection.recv(4096)
            string = json.loads(received_string)
            if string["request"] in self.responses:
                self.responses[string["request"]](string["content"])


    def login(self, content):
        self.name = content
        Users.append(self)
        self.sender("system", "info", "Welcome to the server")

    def logout(self, content):
        pass

    def msg(self, content):
        for user in Users:
            if user != self:
                user.sender(self.name,'message',content)
        pass

    def names(self, content):
        pass

    def helper(self, content):
        pass

    def history(self, content):
        pass

    def sender(self, sender,response, content):
        package = json.dumps({"timestamp": strftime("%Y-%m-%d %H:%M:%S", gmtime()),
            "sender": sender, 
            "response": response,
            "content": content})
        self.connection.send(package)


class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    """
    This class is present so that each client connected will be ran as a own
    thread. In that way, all clients will be served by the server.

    No alterations are necessary
    """
    allow_reuse_address = True

if __name__ == "__main__":
    """
    This is the main method and is executed when you type "python Server.py"
    in your terminal.

    No alterations are necessary
    """
    HOST, PORT = 'localhost', 9998
    print 'Server running...'

    # Set up and initiate the TCP server
    server = ThreadedTCPServer((HOST, PORT), ClientHandler)
    server.serve_forever()
