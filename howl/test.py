import time
import requests


def getip():
    with open('tmp/ip.txt', 'r') as ipf:
        for line in ipf.readlines():
            ip = line.split('\t')
            print('{}-{}'.format(ip[0], ip[1]))
            requests.post(
                'http://127.0.0.1:9900/api/whatweb?netmask=16&ip={}&port=80'.
                format(ip[0]))
            time.sleep(3000)


if __name__ == '__main__':
    getip()