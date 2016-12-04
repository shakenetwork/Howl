from elasticsearch import Elasticsearch
import redis
esserver='127.0.0.1'
es = Elasticsearch(hosts=esserver)
whatwebdb = redis.Redis('127.0.0.1',6379,0,decode_responses=True)