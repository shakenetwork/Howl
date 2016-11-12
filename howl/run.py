from api import app
import sys
from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop

if __name__ == '__main__':
    http_server = HTTPServer(WSGIContainer(app))
    app.debug = False
    port = sys.argv[1]
    http_server.listen(port)
    IOLoop.instance().start()