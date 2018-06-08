# Echart-with-websocket-server
Data Visualization demo with simply python websocket server and Echart JS
数据可视化demo使用python websocket 服务器 和 EchartJS 模板。
运行效果为:websocket形成连接，每隔10秒发送一行数据给客户端
客户端把数据变为数组，实时刷新展示为折现图.

How to use 如何使用?
//0. 运行createrandom.py 生成随机模拟数据集. 

1. Download Echart.JS from Baidu(下载百度EchartJS). http://echarts.baidu.com/download.html

2. Download tornado_websocket.(下载 tornado_websocket). 
pip install tornado

3. 运行tornado_server.py

4. 打开test.html.
