import json
import os
from config import es, whatwebdb

import ipaddress
import redis
from celery import Celery, platforms
from celery.schedules import crontab

platforms.C_FORCE_ROOT = True
app = Celery('tasks', broker='redis://localhost:6379/1')
ip_db = redis.Redis(host='localhost', port=6379, db=2, decode_responses=True)


def remove_tmp(filepath):
    if os.path.exists(filepath):
        os.remove(filepath)


@app.task
def add2whatweb(open_target_path, port):
    whatweb_logfile = '{}_{}.json'.format(open_target_path, port)
    remove_tmp(whatweb_logfile)
    os.system(
        "whatweb -q --no-errors --wait=10 -t 255 -i {} --url-suffix=':{}' --log-json={}".
        format(open_target_path, port, whatweb_logfile))
    with open(whatweb_logfile, 'r') as logf:
        lines = json.load(logf)
        for target in lines:
            save2es(target)
    whatwebdb.decr('scanning')
    remove_tmp(whatweb_logfile)


@app.task
def save2es(target):
    try:
        parse_target = target['target'].split(':')
        if len(parse_target) > 2:
            target['port'] = parse_target[-1].split('/')[0]
        else:
            target['port'] = '80'
        es.index(
            index='whatweb',
            doc_type="detail",
            id=int(
                str(
                    int(
                        ipaddress.IPv4Address(target['plugins']['IP']['string']
                                              [0]))) + target['port']),
            body=target)
        print(target)
    except:
        pass


@app.task
def masscan(target, port):
    whatwebdb.incr('scanning')
    masscan_result_path = '/tmp/tmp_{}_{}'.format(
        target.replace('/', '_'), port)
    results = os.popen(
        'masscan -p{0} {1} --rate=500 -oL {2} && cat {2}'.format(
            port, target, masscan_result_path)).read().split('\n')[1:-2]
    remove_tmp(masscan_result_path)
    for result in results:
        print(result)
        ip = result.split(" ")[3]
        ip_db.sadd('{}_{}'.format(target, port), ip)
    open_target_path = masscan_result_path + '.txt'
    remove_tmp(open_target_path)
    with open(open_target_path, 'a+') as f:
        for i in ip_db.smembers('{}_{}'.format(target, port)):
            f.writelines(i + '\n')
    if len(ip_db.smembers('{}_{}'.format(target, port))):
        add2whatweb(open_target_path, port)
    else:
        whatwebdb.decr('scanning')
