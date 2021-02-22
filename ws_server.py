import tornado.httpserver
import tornado.websocket
import tornado.ioloop
import tornado.web
import socket
'''
This is a simple Websocket Echo server that uses the Tornado websocket handler.
Please run `pip install tornado` with python of version 2.7.9 or greater to install tornado.
This program will echo back the reverse of whatever it recieves.
Messages are output to the terminal for debuggin purposes. 
''' 
ws_clients = []
class WSHandler(tornado.websocket.WebSocketHandler):

    def open(self):
        print('new connection')
        self.write_message("Hello World")
        if self not in ws_clients:
            ws_clients.append(self)
      
    def on_message(self, message):
        print('message received:  %s' % message)
        # Reverse Message and send it back
        #self.write_message(message)
        self.send_message_to_all(message.text)
         
    def on_close(self):
        print('connection closed')
 
    def check_origin(self, origin):
        return True
    def send_message_to_all(self, message):
        for c in ws_clients:
            if self != c:
                c.write_message(message)
 
application = tornado.web.Application([
    (r'/ws', WSHandler),
])
 
 
if __name__ == "__main__":
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(8888)
    myIP = "127.0.0.1"
    print('*** Websocket Server Started at %s***' % myIP)
    tornado.ioloop.IOLoop.instance().start()
