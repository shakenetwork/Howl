from flask import Flask, request, redirect
from flask_restful import Resource, Api, reqparse
from config import es
from tasks import *

app = Flask(__name__)
howlapi = Api(app)


class SubdomainsList(Resource):
    def get(self, domain):
        s = es.search(index="subdomains", q='domain:{}'.format(domain))
        if s['hits']['hits']:
            return s['hits']['hits'][0]['_source']
        else:
            return []


class HowlList(Resource):
    def get(self, query):
        es.indices.create(index="whatweb", ignore=400)
        s = es.search(index="whatweb", q=query, size=10000)
        if s['hits']['hits']:
            hits = []
            for hit in s['hits']['hits']:
                hits.append(hit['_source'])
            return {'count': len(hits), 'data': hits}
        else:
            return []

    def post(self, query):
        es.indices.create(index="whatweb", ignore=400)
        add2whatweb.delay('{}.json'.format(query),query,80)
        return {'code': 200}

howlapi.add_resource(HowlList, '/api/whatweb/<string:query>')
howlapi.add_resource(SubdomainsList, '/api/subdomains/<string:domain>')
