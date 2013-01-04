# -*- coding: utf-8 -*-
import json
import tornado
import sockjs.tornado

from zmq.eventloop import ioloop
from tornado.options import options, define
from djazator import sub

ioloop.install()
io_loop = tornado.ioloop.IOLoop.instance()

class BaseMsgHandler(object):
    """
    Base SockJS connectiont handler.
    Provide your own if you need advanced functionality.
    """

    def __init__(self, connection):
        self.conn = connection # SockJS connection

    def __call__(self, data):
        if not 'name' in data:
            return
        handler_name = data.get('name', '')
        if (handler_name
            and not handler_name.startswith('_')
            and 'data' in data):
            try:
                handler = self.__getattribute__(handler_name)
                return handler(data['data'])
            except AttributeError:
                pass

    def subscribe(self, data):
        """
        Subscribe SockJS connection on token notifications
        """
        if not self.conn.token and 'token' in data:
            self.conn.token = data['token']
            self.conn.mq_sub.add_subscriber(self.conn)


class SockJSConnection(sockjs.tornado.SockJSConnection):

    mq_sub = None # should be initialized by router

    def __init__(self, *args, **kw):
        self.token = None
        self.msg_handler = BaseMsgHandler(self)
        super(SockJSConnection, self).__init__(*args, **kw)

    def on_open(self, info):
        self.mq_sub.add_listener(self)

    def on_close(self):
        self.mq_sub.remove_listener(self)
        if self.token:
            self.mq_sub.unregister(self)

    def on_message(self, message):
        return self.msg_handler(json.loads(message))


class SockJSRouter(sockjs.tornado.SockJSRouter):

    def __init__(self, *args, **kw):
        socket_addr = kw.pop('socket_addr')
        super(SockJSRouter, self).__init__(*args, **kw)
        self._connection.mq_sub = sub.ZeroMQClient(self.io_loop, socket_addr=socket_addr)
        self._connection.mq_sub.connect()

define("port", default=8080, help="run on the given port", type=int)
define("address", default='', help="run on the given address", type=str)
define("mq_socket", type=str, help="socket to bind for django mq notifications")
define("route", default='/sockjs', type=str)

def _run():
    tornado.options.parse_command_line()
    router = SockJSRouter(SockJSConnection,
        options.route,
        socket_addr=options.mq_socket)
    app = tornado.web.Application(router.urls,)
    app.listen(options.port, address=options.address)
    try :
        io_loop.start()
    except KeyboardInterrupt:
        pass

if __name__ == '__main__':
    _run()
