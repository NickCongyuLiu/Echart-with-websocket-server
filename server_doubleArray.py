#coding=utf-8  

import tornado.web
import tornado.ioloop
import tornado.httpserver
import tornado.options
import os
import datetime
import time
import json


from tornado.web import RequestHandler
from tornado.options import define, options
from tornado.websocket import WebSocketHandler



define("port", default=9000, type=int)


class ChatHandler(WebSocketHandler):


    def open(self):

        self.sendFile = []
        self.file_list = []
        self.file_count = 0
        print("connection succeed")

        # 遍历文件夹文件
        rootdir = '/home/minieye/WebSocket/netdig-json-0317'
        fileList = os.listdir(rootdir)
        for i in range(0,len(fileList)):
            filePath = os.path.join(rootdir,fileList[i])
            if os.path.isfile(filePath):
                if(filePath[len(filePath)-4:len(filePath)]!='json'):
                    # print(filePath)
                    pass
                else:
                    self.file_list.append(filePath)

        self.write_message("work")

        # f = open("/home/minieye/WebSocket/netdig-json-0317/川A0C59P_7aad6c4ab393fe52.json")
        # print(f)
        # test = json.load(f)
        # for t in test:
        #     # print(t)
        #     # ts 表示 时间戳 1514736000表示2018-01-01的时间戳，小于这个时间默认网络时间错误
        #     if(t['network_error']!=0 or (('ts' in t) and (t['ts']<1514736000))):
        #         if 'sim_failure' in t:
        #             self.sendFile.append(-t['uptime']-0.2)
        #         else:
        #             self.sendFile.append(-t['uptime']-0.1)
        #     else:
        #         self.sendFile.append(t['uptime'])
        # mess = ''.join(str(e)+" " for e in self.sendFile)
        # # print (mess)
        # self.write_message(mess)


        ##把文件全传到前端
        ##self.write_message(json.dumps(test))
        # for t in test:
        #     print t['uptime']
        # for line in file.readlines(100):
        #     self.write_message(line)
        #     # time.sleep(10)
        # file.close() 

    def on_message(self, message):
        # print("received message "+message)
        
        if(message=="123"):
            time.sleep(5)
            if(self.file_count<len(self.file_list)):
                f = open(self.file_list[self.file_count])
                # print(self.file_count)
                print(self.file_list[self.file_count])
                test = json.load(f)
                for t in test:
                    # print(t)
                    # ts 表示 时间戳 1514736000表示2018-01-01的时间戳，小于这个时间默认网络时间错误
                    if('uptime' not in t):
                        pass
                    elif(t['network_error']!=0 or (('ts' in t) and (t['ts']<1514736000))):
                        if 'sim_failure' in t:
                            self.sendFile.append(-t['uptime']-0.2)
                        else:
                            self.sendFile.append(-t['uptime']-0.1)
                    else:
                        self.sendFile.append(t['uptime'])
                mess = ''.join(str(e)+" " for e in self.sendFile)
                self.sendFile =[]
                for t in test:
                    if('uptime' not in t):
                        pass
                    elif('ts' in t):
                        self.sendFile.append(t['ts'])
                    else:
                        self.sendFile.append('0')
                mess = mess +''.join(str(e)+" " for e in self.sendFile)
                mess = mess + ' '+self.file_list[self.file_count]
                # print (mess)
                self.write_message(mess)
                f.close()
                self.sendFile=[]
                self.file_count+=1
            else:
                self.on_close
        pass
        
    def on_close(self):
        print('connection closed')
        pass

    def check_origin(self, origin):
        return True  # 允许WebSocket的跨域请求

if __name__ == '__main__':
    tornado.options.parse_command_line()
    app = tornado.web.Application([
            (r"/chat", ChatHandler),
        ],
        static_path = os.path.join(os.path.dirname(__file__), "static"),
        template_path = os.path.join(os.path.dirname(__file__), "template"),
        debug = True
        )
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.current().start()

