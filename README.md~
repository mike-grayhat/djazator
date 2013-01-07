djazator
========

[djazator](https://github.com/mike-grayhat/djazator) is a simple django plugin for sending push messages from django server to sockjs clients. It internally uses [zeromq](http://www.zeromq.org/) and [sockjs-tornado](https://github.com/mrjoes/sockjs-tornado). djazator can send push notifications to all sockjs clients and to subset of this clients.

##Requirements:

1. [pyzmq](https://github.com/zeromq/pyzmq)>=2.0
2. [sockjs-tornado](https://github.com/mrjoes/sockjs-tornado)>=0.0.5
3. [django](https://www.djangoproject.com/)>=1.4

##Installation:

1. Install `djazator` with your favorite Python package manager:

        pip install djazator

2. Add `djazator` to your INSTALLED_APPS in `settings.py`

        INSTALLED_APPS = (
            'django.contrib.auth',
            'djazator',
            ...
        )

3. define DJAZATOR_MQ_SOCKET in `settings.py`

        DJAZATOR_MQ_SOCKET = 'tcp://127.0.0.1:8001'

## Usage:

1. run sockjs-tornado server

        python -m djazator.server --port=8080 --mq_socket=tcp://127.0.0.1:8001 --route=/sockjs --address=''

2. append sockjs client library to your page

        <head>
            <script src="http://cdn.sockjs.org/sockjs-0.3.min.js">
            ...

3. open page in browser and connect to sockjs-tornado server

        conn = new SockJS('http://localhost:8080/sockjs')

4. define a callback for incoming messages

        conn.onmessage = function (e){ console.log(e.data); };

5. send a message from django

        from djazator.pub import notify_all
        notify_all({'msg': u'Hi all!'})

    and you will see it in js console

            Object {msg: "Hi all!"}

## Advanced notifications:

You can send notifications to only dedicated users.

    from djazator.pub import notify
    from djazator.utils import tokenize
    from django.contrib.auth.models import User
    user = User.objects.get(email='djazator@mail.com')
    notify({'msg': u'Hi, %s!' % user.username}, recipients=[user])
    token = tokenize(user)
    notify({'msg': u'Hi user with token %s !' % token}, recipients=[user])

To get this messages you need to subscribe by token

    var token = {% djazator_token %};
    SockJS.prototype.emit = function (name, data) {
        var meta_dict = {
            name:name,
            data:data
        };
        this.send(JSON.stringify(meta_dict))
    };
    conn = new SockJS('http://localhost:8080/sockjs')
    conn.emit('subscribe', {'token': token});
    conn.onmessage = function (e){ console.log(e.data); };

`{% djazator_token %}` is nothing more than a wrapper around `djazator.utils.tokenize` that only returns `user.id`. You need to provide your own tokenization function for better security. It should accept django User object and return token. Add path to this function in settings.py .

    DJAZATOR_TOKENIZER = 'path.to.my.func'

## Limitations:

Now djazator supports only one tornado instance. I'm planning to implement multiple tornado instances through zeromq dealer/poller in future versions.

## Production:

1. [Hipache](https://github.com/dotcloud/hipache)
