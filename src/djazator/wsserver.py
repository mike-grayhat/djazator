# -*- coding: utf-8 -*-
"""
    Simple sockjs-tornado chat application. By default will listen on port 8080.
"""
import json
import tornado
import sockjs.tornado
import sub

from zmq.eventloop import ioloop
from tornado.options import options, define

ioloop.install()
io_loop = tornado.ioloop.IOLoop.instance()

class BaseClientHandler(object):

    def __init__(self, connection):
        self.connection = connection

    def __call__(self, data):
        if not 'method' in data:
            return
        handler_name = data.get('method')
        if not handler_name.startswith('_'):
            handler = self.__getattribute__(handler_name)
            return handler(data['data'])


class SockJSConnection(sockjs.tornado.SockJSConnection):

    mq_subscription = None # initialized by router

    def on_open(self, info):
        self.mq_subscription.add_listener(self)

    def on_close(self):
        self.mq_subscription.remove_listener(self)
        if self.client_id:
            self.mq_subscription.unregister(self)

    def on_message(self, message):
        msg = json.loads(message)
        data = msg['data']
        if msg.get('name') == 'authenticate':
            self.authenticate(data)
        return self.client_handler(data)

    def authenticate(self, data):
        if not self.client_id and 'client_id' in data:
            self.client_id = data['client_id']
            self.mq_subscription.register(self)

    def __init__(self, *args, **kw):
        self.client_id = None
        self.client_handler = BaseClientHandler(self)
        super(SockJSConnection, self).__init__(*args, **kw)


class SockJSRouter(sockjs.tornado.SockJSRouter):

    def __init__(self, *args, **kw):
        socket_addr = kw.pop('socket_addr')
        super(SockJSRouter, self).__init__(*args, **kw)
        self._connection.mq_subscription = sub.ZeroMQClient(self.io_loop, socket_addr=socket_addr)
        self._connection.mq_subscription.connect()


define("port", default=8080, help="run on the given port", type=int)
define("address", default='', help="run on the given address", type=str)
define("mq_socket", type=str, help="socket to bind for django mq notifications")
define("route", default='/', type=str)

def _runserver():
    tornado.options.parse_command_line()
    router = SockJSRouter(SockJSConnection,
        options.route,
        socket_addr=options.mq_socket)
    app = tornado.web.Application(router.urls,)
    app.listen(options.port, address=options.address)
    io_loop.start()

if __name__ == '__main__':
    _runserver()
