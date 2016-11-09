# Howl

# Usage:
```bash
$python3 whatweb2es.py -h
optional arguments:
  -h, --help  show this help message and exit
  -f F        log file
  -s S        Elasticsearch Server
  -i I        Elasticsearch Index
```

 - 用 `whatweb` 进行 web 服务指纹扫描(扫描10.11.1.1/16的8080端口，并保存结果为10.11.json)

 ```
 $whatweb --no-errors -t 255 10.11.1.1/16 --url-suffix=':8080' --log-json=10.11.json
 ```

 - 导入elasticsearch
 
 ```bash
 $python3 whatweb2es.py -f 10.11.json
 ```

