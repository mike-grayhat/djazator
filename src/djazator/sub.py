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
        self.listeners = set()
        self.subscribers = defaultdict(set)

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
            subscribers_ids = self.subscribers.get(r, [])
            for conn in subscribers_ids:
                conn.send(data)

    def notify_all(self, data):
        for c in self.listeners:
            c.send(data)

    def add_subscriber(self, client):
        if client.token:
            self.subscribers[client.token].add(client)

    def remove_subscriber(self, client):
        try:
            self.subscribers[client.token].remove(client)
        except KeyError:
            pass

    def add_listener(self, client):
        self.listeners.add(client)

    def remove_listener(self, client):
        self.listeners.remove(client)
