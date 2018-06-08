#coding=utf-8  

import tornado.web
import tornado.ioloop
import tornado.httpserver
import tornado.options
import os
import datetime
import time

from tornado.web import RequestHandler
from tornado.options import define, options
from tornado.websocket import WebSocketHandler

define("port", default=5000, type=int)

class IndexHandler(RequestHandler):
    def get(self):
        self.render("index.html")

class ChatHandler(WebSocketHandler):

    users = set()  # 用来存放在线用户的容器

    def open(self):
        self.users.add(self)  # 建立连接后添加用户到容器中
        print("connection succeed")
        for u in self.users:  # 向链接用户发送数据
            file = open("/home/minieye/WebSocket/testdata")
            while 1:
                lines = file.readlines(100)
                if not lines:
                    break
                for line in lines:
                    u.write_message(line)
                    time.sleep(10)
            file.close() 

    def on_message(self, message):
        # print(message)
        pass
        # for u in self.users:  # 向在线用户广播消息
            # u.write_message(u"[%s]-[%s]-说：%s" % (self.request.remote_ip, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), message))

    def on_close(self):
        self.users.remove(self) # 用户关闭连接后从容器中移除用户
        pass
        # for u in self.users:
            # u.write_message(u"[%s]-[%s]-离开" % (self.request.remote_ip, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))

    def check_origin(self, origin):
        return True  # 允许WebSocket的跨域请求

if __name__ == '__main__':
    tornado.options.parse_command_line()
    app = tornado.web.Application([
            (r"/", IndexHandler),
            (r"/chat", ChatHandler),
        ],
        static_path = os.path.join(os.path.dirname(__file__), "static"),
        template_path = os.path.join(os.path.dirname(__file__), "template"),
        debug = True
        )
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.current().start()