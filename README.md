# tornado-Echart
tornado-Echart 是一个数据可视化的工具。
v0.1
:toc:

:numbered:


### 依赖

* tornaodo_websocket
* echartJS4.1.0.rc2
* Jquery1.4
* python 3.5.2

安装 

```shell
cd ./home/minieye 进入minieye文件夹
mkdir Websocket 创建Websocket文件夹
下载EchartJS源代码包(Echart.js)到/home/minieye/Websocket/目录下
下载安装tornado
pip install tornado
```

### 使用

#### 下载代码

打开网页https://github.com/NickCongyuLiu/Echart-with-websocket-server
下载程序到/home/minieye/Websocket/目录下


#### 运行

```shell
usage: python3 tornado server.py

```
双击打开main_server.html,点击连接 即可以看见实时更新的折线图.
设置chrome浏览器：
1.进入设置-高级-内容设置-自动下载项-允许-添加-file://home/minieye/Websocket/main.html
2.进入设置-高级-下载内容-下载前询问每个文件的保存位置-关闭
配置路径：
打开main_server.py，
将第32行rootdir=‘’ 相应的ht包文件夹路径（注：是文件夹路径，包含所有将展示的json文件）
将第61行filePath=‘’ 相应的心跳包文件夹路径
