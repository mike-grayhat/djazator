djazator
========

`djazator`_ is a simple django plugin for sending push messages from
django server to sockjs clients. It internally uses `zeromq`_ and
`sockjs-tornado`_. djazator can send push notifications to all sockjs
clients and to subset of this clients.

Requirements:
-------------

1. `pyzmq`_>=2.0
2. `sockjs-tornado`_>=0.0.5
3. `django`_>=1.4

Installation:
-------------

Install ``djazator`` with your favorite Python package manager:

::

   pip install djazator

Add ``djazator`` to your ``INSTALLED_APPS`` in ``settings.py``

::

   INSTALLED_APPS = (
       'django.contrib.auth',
       'djazator',
       ...
   )

Define ``DJAZATOR_MQ_SOCKET`` in ``settings.py``

::

   DJAZATOR_MQ_SOCKET = 'tcp://127.0.0.1:8002'

Usage:
------

Run sockjs-tornado server

::

   djazator-server --port=8080 --mq_socket=tcp://127.0.0.1:8001 --route=/sockjs --address=''

Run zeromq forwarder device

::

   djazator-mq --sub=tcp://127.0.0.1:8002 --pub=tcp://127.0.0.1:8001

Append sockjs client library to your page

::

   <head>
       <script src="http://cdn.sockjs.org/sockjs-0.3.min.js">
       ...

Open page in browser and connect to sockjs-tornado server

::

   conn = new SockJS('http://localhost:8080/sockjs')

Define a callback for incoming messages

::

   conn.onmessage = function (e){ console.log(e.data); };

Send a message from django

::

   from djazator.pub import notify_all
   notify_all({'msg': u'Hi all!'})

and you will see it in js console

::

       Object {msg: "Hi all!"}

Advanced notifications:
-----------------------

You can send notifications to only dedicated users.

::

    from djazator.pub import notify
    from djazator.utils import tokenize
    from django.contrib.auth.models import User
    user = User.objects.get(email='djazator@mail.com')
    notify({'msg': u'Hi, %s!' % user.username}, users=[user])
    token = tokenize(user)
    notify({'msg': u'Hi user with token %s !' % token}, users=[user])

To get this messages you need to subscribe by token

::

    var token = {% djazator_token %};
    SockJS.prototype.emit = function (name, data) { // wrapper around SockJS.send for djazator's protocol support
        var meta_dict = {
            name:name,
            data:data
        };
        this.send(JSON.stringify(meta_dict))
    };
    conn = new SockJS('http://localhost:8080/sockjs')
    conn.emit('subscribe', {'token': token});
    conn.onmessage = function (e){ console.log(e.data); };

``{% djazator_token %}`` is nothing more than a wrapper around
``djazator.utils.tokenize`` that only returns ``user.id``. You need to
provide your own tokenization function for better security. It should
accept django User object and return token. Add path to this function in
settings.py .

::

    DJAZATOR_TOKENIZER = 'path.to.my.func'

Conclusions:
------------

1. djazator serializes datetime objects with ISO 8601 format. You can parse it on client with `moment.js`_ .
2. djazator server can handle client's messages constructed only in some specific way and can't be used for client to client communications.

Production:
-----------

1. `Hipache`_

.. _djazator: https://github.com/mike-grayhat/djazator
.. _zeromq: http://www.zeromq.org/
.. _moment.js: http://momentjs.com/
.. _sockjs-tornado: https://github.com/mrjoes/sockjs-tornado
.. _pyzmq: https://github.com/zeromq/pyzmq
.. _django: https://www.djangoproject.com/
.. _Hipache: https://github.com/dotcloud/hipache