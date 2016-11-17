# -*- coding: utf-8 -*-

from flask import Flask, request, redirect, render_template
from flask_restful import Resource, Api, reqparse
from flask_restful.utils import cors
from flask_cors import CORS, cross_origin
from config import es, whatwebdb
from tasks import *

app = Flask(__name__)
CORS(app)
howlapi = Api(app)


class VuldbList(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('limit', type=int, help='limit必须为int', default=1)
        parser.add_argument('q', type=str, help='请输入有效域名')
        args = parser.parse_args()
        s = es.search(
            index="vuldb",
            q='title:{}'.format(args.q),
            size=args.limit,
            sort='time:desc'
            )
        if s['hits']['hits']:
            hits = []
            for hit in s['hits']['hits']:
                hits.append(hit['_source'])
            return {'count': len(hits), 'data': hits}
        else:
            return []


class SubdomainsList(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('limit', type=int, help='limit必须为int', default=1)
        parser.add_argument('q', type=str, help='请输入有效域名')
        args = parser.parse_args()
        s = es.search(
            index="subdomains",
            q='domain:{}'.format(args.q),
            size=args.limit)
        if s['hits']['hits']:
            hits = []
            for hit in s['hits']['hits']:
                hits.append(hit['_source'])
            return {'count': len(hits), 'data': hits}
        else:
            return []


class HowlList(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('limit', type=int, help='limit必须为int', default=100)
        parser.add_argument('q', type=str, help='请输入有效查询')
        args = parser.parse_args()
        s = es.search(index="whatweb", q=args.q, size=args.limit)
        if s['hits']['hits']:
            hits = []
            for hit in s['hits']['hits']:
                hits.append(hit['_source'])
            return {'count': len(hits), 'data': hits}
        else:
            return []

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument(
            'netmask', type=int, help='netmask必须为int', default=24)
        parser.add_argument('ip', type=str, help='请输入有效ip')
        parser.add_argument('port', type=int, help='请输入有效port', default=80)
        args = parser.parse_args()
        print(args)
        target = '{}/{}'.format(args.ip, args.netmask)
        if not whatwebdb.exists('scanning'):
            whatwebdb.set('scanning', 0)
        if '{}_{}'.format(
                target,
                args.port).encode('ascii') in whatwebdb.smembers('scaned'):
            print(target)
            return {'code': 201}
        elif int(whatwebdb.get('scanning')) < 3:
            add2whatweb.delay(target, args.port)
            return {'code': 202}
        else:
            add2whatweb.apply_async(
                (target,
                 args.port, ),
                countdown=int(whatwebdb.get('scanning')) * 600)
            return {'code': 202}

howlapi.add_resource(VuldbList, '/api/vuldb')
howlapi.add_resource(HowlList, '/api/whatweb')
howlapi.add_resource(SubdomainsList, '/api/subdomains')


@app.route('/')
def index():
    return render_template('index.html')