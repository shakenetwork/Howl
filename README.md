## 网络设备 web 服务指纹扫描与检索

### 实现思路:

利用 flask 开放 api，通过调用 api 来实现添加任务或数据检索;利用 celery 来进行异步调用 whatweb 来进行扫描，然后保存数据到 elasticsearch

相关 api：

- 添加任务(扫描10.1.1.1/16段内开放80 端口的web 服务指纹) : `POST http://host:port/api/whatweb?netmask=16&ip=10.1.1.1&port=80` 
- 查询数据(关键字 kibana) : `GET http://host:port/api/whatweb?q=kibana`
### 依赖:

- elasticsearch
- redis
- python3
- whatweb

### 安装:
```
$ virtualenv --python=/somepath/python3.5 venv
$ source venv/bin/activate
$ pip install -r requirements.txt
```
### 运行:

```
$ cd howl
$ python run.py 端口
```

### 截图:

![](http://obfxuk8r6.bkt.clouddn.com/demo.png)