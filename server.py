import time
from SimpleWebSocketServer import SimpleWebSocketServer, WebSocket

class SimpleEcho(WebSocket):

    def handleMessage(self):
        # echo message back to client
        # self.sendMessage(self.data)
        print(self.data)

    def handleConnected(self):
        print(self.address, 'connected')
        file = open("/home/minieye/WebSocket/testdata")
        while 1:
            lines = file.readlines(100)
            if not lines:
                break
            for line in lines:
                self.sendMessage(line)
        file.close() 
        

    def handleClose(self):
        print(self.address, 'closed')

server = SimpleWebSocketServer('', 8000, SimpleEcho)
server.serveforever()

# from SimpleWebSocketServer import SimpleWebSocketServer, WebSocket

# clients = []
# class SimpleChat(WebSocket):

#     def handleMessage(self):
#        for client in clients:
#           if client != self:
#              client.sendMessage(self.address[0] + u' - ' + self.data)

#     def handleConnected(self):
#        print(self.address, 'connected')
#        for client in clients:
#           client.sendMessage(self.address[0] + u' - connected')
#        clients.append(self)

#     def handleClose(self):
#        clients.remove(self)
#        print(self.address, 'closed')
#        for client in clients:
#           client.sendMessage(self.address[0] + u' - disconnected')



# server = SimpleWebSocketServer('', 8000, SimpleChat)
# server.serveforever()