import time
import requests


def getip():
    with open('tmp/china_ip_list.txt', 'r') as ipf:
        for line in ipf.readlines():
            ip = line.strip('\n').split('/')
            requests.post(
                'http://127.0.0.1:9900/api/whatweb?netmask={}&ip={}&port=80'.
                format(ip[1],ip[0]))
            time.sleep(10)


if __name__ == '__main__':
    getip()