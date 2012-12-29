import json
import zmq

from collections import defaultdict
from zmq.eventloop.zmqstream import ZMQStream

ctx = zmq.Context()

class ZeroMQClient(object):

    def __init__(self, io_loop, socket_addr):
        self.io_loop = io_loop
        self.connected = False
        self.socket = None
        self.socket_addr = socket_addr
        self.clients = set()
        self.registered_clients = defaultdict(set)

    def connect(self):
        if self.connected:
            return
        self.socket = ctx.socket(zmq.SUBSCRIBE)
        self.socket.bind(self.socket_addr)
        stream = ZMQStream(self.socket, self.io_loop)
        stream.on_recv(self.on_message)
        self.connected = True

    def on_closed(self, connection):
        self.io_loop.stop()

    def on_message(self, body):
        msg = json.loads(body[1])
        data = msg.pop('data')
        handler_name = msg.pop('name')
        handler = getattr(self, handler_name, None)
        if callable(handler):
            handler(data, **msg)

    def notify(self, data, recipients=tuple()):
        for r in recipients:
            client_id_listeners = self.registered_clients.get(r, [])
            for conn in client_id_listeners:
                conn.send(data)

    def notify_all(self, data):
        for c in self.clients:
            c.send(data)

    def notify_listeners(self, event_obj):
        for listener in self.registered_clients.values():
            listener.push(event_obj)

    def register(self, listener):
        if listener.client_id:
            self.registered_clients[listener.client_id].add(listener)

    def add_listener(self, listener):
        self.clients.add(listener)

    def remove_listener(self, listener):
        self.clients.remove(listener)

    def unregister(self, listener):
        try:
            self.registered_clients[listener.client_id].remove(listener)
        except KeyError:
            pass
