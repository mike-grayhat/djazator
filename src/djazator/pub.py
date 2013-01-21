import zmq
import json
import datetime

from django.conf import settings
from django.utils import timezone

from .utils import tokenize

__all__ = ('notify', 'notify_all')

ctx = zmq.Context()
_current_timezone = timezone.get_current_timezone()

def _dthandler(obj):
    if isinstance(obj, datetime.datetime):
        return _current_timezone.localize(obj).isoformat()
    return None

def _get_send_json_method():
    if settings.DEBUG:
        def dev(json_data):
            """Handle zeromq socket error on django server reloading"""
            socket = ctx.socket(zmq.PUB)
            socket.connect(settings.DJAZATOR_MQ_SOCKET)
            socket.send(json_data, zmq.NOBLOCK)
            socket.close()
        return dev
    else:
        socket = ctx.socket(zmq.PUB)
        socket.connect(settings.DJAZATOR_MQ_SOCKET)
        def production(json_data):
            socket.send(json_data, zmq.NOBLOCK)
        return production

send_json_data = _get_send_json_method()

def send_data(data, default_serializer=_dthandler):
    json_data = json.dumps(data, default=default_serializer)
    send_json_data(json_data)

def notify(data, users=tuple(), serializer=_dthandler, **kw):
    client_hashes = [tokenize(u) for u in users]
    msg = {'data': data,
           'name': 'notify',
           'recipients': client_hashes}
    msg.update(**kw)
    send_data(msg, default_serializer=serializer)

def notify_all(data, **kw):
    msg = {'data': data,
           'name': 'notify_all',
           }
    msg.update(**kw)
    send_data(msg)
