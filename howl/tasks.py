from celery import Celery, platforms
from config import es
import os
import json
import ipaddress
platforms.C_FORCE_ROOT = True
app = Celery('tasks', broker='redis://localhost')


@app.task
def add2whatweb(logfile, target, port):
    if os.path.exists(logfile):
        os.system('rm {}'.format(logfile))
    os.system("whatweb --no-errors -t 255 {} --url-suffix=':{}' --log-json={}".
              format(target, port, logfile))
    with open(logfile, 'r') as logf:
        lines = json.load(logf)
        for line in lines:
            save2es.delay(line)


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