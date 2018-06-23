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



define("port", default=9999, type=int)


class ChatHandler(WebSocketHandler):

    #建立websocket连接
    def open(self):

        self.sendFile = []
        self.file_list = []
        self.file_count = 0
        self.rootdir=''
        print("connection succeed")

        rootdir = os.getcwd()+'/analysis_recent_result'
        fileList = os.listdir(rootdir)
        fileList_mess = ''.join(str(e)+" " for e in fileList)
        fileList_mess = fileList_mess+'fileList'
        self.write_message(fileList_mess)

        # # 遍历ht包文件夹文件
        # rootdir = '/home/minieye/WebSocket/analysis_recent_result/2018-06-16'
        # fileList = os.listdir(rootdir)
        # for i in range(0,len(fileList)):
        #     filePath = os.path.join(rootdir,fileList[i])
        #     if os.path.isfile(filePath):
        #         #如果不是json文件直接跳过
        #         if(filePath[len(filePath)-4:len(filePath)]!='json'):
        #             pass
        #         else:
        #             self.file_list.append(filePath)
        # #给前端发送信号
        # self.write_message("work")

    #websocket接受信息
    def on_message(self, message):


        ##展示文件
        if(message[0:12]=='ask for fold'):
            file_list_mess =[]
            # print(message[13:])
            self.file_list=[]
            self.rootdir = os.getcwd()+'/analysis_recent_result/'+message[13:]
            fileList = os.listdir(self.rootdir)
            for i in range(0,len(fileList)):
                filePath = os.path.join(self.rootdir,fileList[i])
                if os.path.isfile(filePath):
                    #如果不是Json文件直接跳过
                    if(filePath[len(filePath)-4:len(filePath)]!='json'):
                        pass
                    else:
                        self.file_list.append(filePath)
        
            # print(self.file_list)
            file_list_mess = ''.join(str(e[-12:-5])+" " for e in self.file_list)
            file_list_mess = file_list_mess+'file'
            self.write_message(file_list_mess)

        #检查自动播放信号 依次发送文件到前端展示        
        if(message[0:12]=='ask for auto'):
            time.sleep(2)
            if(self.file_count<len(self.file_list)):
                f = open(self.file_list[self.file_count])
                test = json.load(f)
                for data in test["data"]:
                    self.sendFile.append(data[0])
                    self.sendFile.append(data[1])
                f.close()
                #获取文件名
                fileName = self.file_list[self.file_count][-12:]
                #在heartbeat文件夹里找寻相同文件名的文件
                filePath = self.rootdir.replace('analysis_recent_result','analysis_heartbeat_result')+'/'+fileName
                # filePath ='/home/minieye/WebSocket/analysis_heartbeat_result/2018-06-16/'+fileName
                try:
                    f =open(filePath)
                    test = json.load(f)
                    for data in test["data"]:
                        #用负数区分heartbeat和汇通
                        self.sendFile.append(-data[0])
                        self.sendFile.append(-data[1])
                except IOError:
                    print(fileName+" 在心跳包文件夹里没有发现对应的文件名")
                # f.close()

                #转换格式方便websocket发送，减轻负担
                mess = ''.join(str(e)+" " for e in self.sendFile)
                #把文件名放在最后
                mess = mess.rstrip()+ ' '+fileName
                #更新需要重复使用的变量
                self.sendFile=[]
                self.file_count+=1
                #发送文件名
                self.write_message(mess)
            else:
                self.on_close
        pass

        ##展示单个json文件
        if(message[0:12]=='ask for json'):
            jsonFile = self.rootdir +'/'+ message[13:]+'.json'
            f=open(jsonFile)
            test = json.load(f)
            single=[]
            for data in test["data"]:
                single.append(data[0])
                single.append(data[1])
            f.close()
            hb_jsonFile = jsonFile.replace('analysis_recent_result','analysis_heartbeat_result')            
            try:
                f=open(hb_jsonFile)
                test = json.load(f)
                for data in test["data"]:
                    single.append(-data[0])
                    single.append(-data[1])
            except IOError:
                print(message[13:]+" 在心跳包文件夹里没有发现对应的文件名")
            f.close()
            #转换格式方便websocket发送，减轻负担
            mess = ''.join(str(e)+" " for e in single)
            #把文件名放在最后
            mess = mess+message[13:]+' '+'singleDisplay'
            self.write_message(mess)
        
    #关闭websocket    
    def on_close(self):
        print('connection closed')
        pass

    #允许跨域请求
    def check_origin(self, origin):
        return True  

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
