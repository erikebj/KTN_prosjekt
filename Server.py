# -*- coding: utf-8 -*-
import SocketServer
import json
from time import gmtime, strftime, sleep

"""
Variables and functions that must be used by all the ClientHandler objects
must be written here (e.g. a dictionary for connected clients)
"""

users = []
history = []
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
        while True:
            # Loop that listens for messages from the client
            received_string = self.connection.recv(4096)
            string = json.loads(received_string)
            if string["request"] in self.responses:
                self.responses[string["request"]](string["content"])

    def formatMessage(self, sender, response, content):
        return json.dumps({"timestamp": strftime("%H:%M:%S", gmtime()),
            "sender": sender, 
            "response": response,
            "content": content})

    def login(self, content):
        self.name = content
        users.append(self)
        self.sender("system", "info", "Welcome to the server " + self.name)
        if len(history) != 0:
            self.history(None)

    def logout(self, content):
        users.remove(self)

    def msg(self, content):
        history.append(self.formatMessage(self.name, "message", content))
        for user in users:
            if user != self:
                user.sender(self.name, "message", content)

    def names(self, content):
        alle = "Users in you channel: "
        for user in users:
            alle += user.name
            alle += ", "
        alle = alle[:-2]
        self.sender("system", "info", alle)

    def helper(self, content):
        helpString = """Command list:
        logout      - Log out of channel.
        history     - Entire chat history.
        help        - This message.
        names       - Participants."""
        self.sender("system", "info", helpString)


    def history(self, content):
        self.sender("system", "history", history)
        #for melding in history:
        #    self.connection.send(melding)
        

    def sender(self, sender,response, content):
        package = self.formatMessage(sender, response, content)
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
    HOST, PORT = '', 9998
    print 'Server running...'

    # Set up and initiate the TCP server
    server = ThreadedTCPServer((HOST, PORT), ClientHandler)
    server.serve_forever()
