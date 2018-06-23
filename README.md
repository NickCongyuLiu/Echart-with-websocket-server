# tornado-Echart
tornado-Echart 是一个数据可视化的工具。
v0.1


### 依赖

* tornaodo_websocket
* echartJS4.1.0.rc2
* Jquery1.4
* python 3.5.2



### 使用
安装 

```shell

https://github.com/NickCongyuLiu/Echart-with-websocket-server
下载EchartJS源代码包(Echart.js)到当前工作目录路径下

下载安装tornado
pip install tornado
```


#### 运行

```shell
usage: python3 main_server.py

```
双击打开main_server.html,点击connnect 即会展示工作路径/analysis-recent-result所包含的所有目录 按日期区分.


#### 文件
客户端页面为main.html文件，包含html,javascript和css. 包含功能有 单个展示单车数据和自动展示日期文件夹数据.
服务端页面为main_server.py文件，包含数据读取 处理 和 与客户端交互等功能

#### 说明

单击任一目录,交互得到所有Json文件名(即单车速度数据).
单击任一单车数据，即可得到此单车数据折线图.
单击自动播放,即可自动播放此日期目录下所有单车速度数据折线图.

左上角显示文件名.
右上角有用户自动下载保存按钮.
