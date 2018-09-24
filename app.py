#!/usr/bin/python

import tornado.httpserver
import sys
from tornado.wsgi import WSGIContainer
from tornado.ioloop import IOLoop
from tornado.web import FallbackHandler, RequestHandler, Application
from appflask import app

class MainHandler(RequestHandler):
  def get(self):
    self.write("Tornado Starting ^_^")

tr = WSGIContainer(app)

application = Application([
(r"/tornado", MainHandler),
(r".*", FallbackHandler, dict(fallback=tr)),
])

def main(argv):
    port = ''
    try:
        port = int(sys.argv[1])
    except:
        port=8090

    application.listen(port=port, address='localhost')
    print("Tornado Web Server running on port:",port)
    IOLoop.instance().start()

if __name__ == "__main__":

 	main(sys.argv)  
