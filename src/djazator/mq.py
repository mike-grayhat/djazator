import zmq
import argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--sub', help='django subscription socket', type=str, required=True)
    parser.add_argument('-p', '--pub', help='tornado publication socket', type=str, required=True)
    args = parser.parse_args()

    ctx = zmq.Context()

    django_sub = ctx.socket(zmq.SUB)
    django_sub.bind(args.sub)
    django_sub.setsockopt(zmq.SUBSCRIBE, "")

    tornado_pub = ctx.socket(zmq.PUB)
    tornado_pub.bind(args.pub)

    try:
        dev = zmq.device(zmq.FORWARDER, django_sub, tornado_pub)
    except KeyboardInterrupt:
        pass

if __name__ == '__main__':
    main()
