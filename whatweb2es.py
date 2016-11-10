from elasticsearch import Elasticsearch
from multiprocessing import Pool
import argparse
import json
import ipaddress


def save2es(target, esindex):
    try:
        parse_target = target['target'].split(':')
        if len(parse_target) > 2:
            target['port'] = parse_target[-1].split('/')[0]
        else:
            target['port'] = '80'
        es.index(
            index=esindex,
            doc_type="detail",
            id=int(
                str(
                    int(
                        ipaddress.IPv4Address(line['plugins']['IP']['string'][
                            0]))) + target['port']),
            body=target)
        print(target)
    except:
        pass


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='import whatweb log to Elasticsearch, by:orange')
    parser.add_argument('-f', help='log file', default='/tmp/whatweb_tmp.json')
    parser.add_argument('-s', help='Elasticsearch Server', default='127.0.0.1')
    parser.add_argument('-i', help='Elasticsearch Index', default='whatweb')
    args = parser.parse_args()
    logfile = args.f
    esserver = args.s
    esindex = args.i
    es = Elasticsearch(hosts=esserver)
    es.indices.create(index=esindex, ignore=400)
    p = Pool(20)
    with open(logfile, 'r') as logf:
        targets = json.load(logf)
        for target in targets:
            p.apply_async(save2es(target, esindex))
    p.close()
    p.join()
