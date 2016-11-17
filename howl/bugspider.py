from requests import *
import re
import argparse
from multiprocessing import Pool
from user_agent import generate_user_agent
from elasticsearch import Elasticsearch
import time

es = Elasticsearch(hosts='127.0.0.1')
es.indices.create(index='vuldb', ignore=400)
seebug_baseurl = 'https://www.seebug.org'
seebug_url = 'https://www.seebug.org/vuldb/vulnerabilities?page'
seebug_pattern = '<a class="vul-title" title=".*?" href="(/vuldb/ssvid-.*?">.*?)</a>'


def spider(page):
    time.sleep(6)
    headers = {'User-Agent': generate_user_agent()}
    print('Fetching Page {}\n====================='.format(page))
    resp = get('{}={}'.format(seebug_url, page), headers=headers).text
    b = resp.split('</tr>')[1:-1]
    for each in b:
        bugs = re.findall(seebug_pattern, each)
        bugtime = re.findall('(\d+-\d+-\d+)', each)[0]
        timestamp = time.mktime(time.strptime(bugtime, '%Y-%m-%d'))
        for bug in bugs:
            title = bug.split('">')[1]
            ssvid = bug.split('">')[0]
            bugid = ssvid.split('-')[1]
            es.index(
                index='vuldb',
                doc_type='vulnerabilities',
                id='ssvid-{}'.format(bugid),
                timestamp=int(timestamp),
                body={'title': title,
                      'time': bugtime,
                      'reference': seebug_baseurl + ssvid,
                      'source': 'seebug'})
        print('{}\t{}'.format(title, ssvid))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Search vuls')
    parser.add_argument('-f', help='from page', default=1)
    parser.add_argument('-t', help='to page', default=3)
    args = parser.parse_args()
    p = Pool(1)
    for page in range(int(args.f), int(args.t) + 1):
        p.apply_async(spider, (page, ))
    p.close()
    p.join()
