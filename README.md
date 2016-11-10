# Howl

# Usage:

```bash
$ python3 howl.py -h
usage: howl.py [-h] [-f F] [-t T] [-p P]

howl

optional arguments:
  -h, --help  show this help message and exit
  -f F        log file
  -t T        target
  -p P        http port
```

```bash
$ python3 whatweb2es.py -h
optional arguments:
  -h, --help  show this help message and exit
  -f F        log file
  -s S        Elasticsearch Server
  -i I        Elasticsearch Index
```

### 用 `whatweb` 进行 web 服务指纹扫描(扫描10.11.1.1/16的8080端口，并保存结果为10.11.json)

```bash
$ python3 howl.py -t 10.11.1.1/16 -f 10.11.json -p 8080
```

### 导入到elasticsearch
 
```bash
$p ython3 whatweb2es.py -f 10.11.json
```

### 利用 kibana 进行查询

![](http://obfxuk8r6.bkt.clouddn.com/Howl.png)