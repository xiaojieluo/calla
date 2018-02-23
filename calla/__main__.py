import argparse
import sys, os
from calla import make_app
from calla.config import Config
from calla.process import start_thread, log_worker


def parse_args(args):
    ''' parse args'''
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-p', '--port', nargs='?', type=int)
    parser.add_argument('-c', '--config', nargs='?', type=str)

    args = parser.parse_args(args)
    return args

def init():
    ''' 初始化工作目录'''
    pass

def main():
    '''enter'''
    args = parse_args(sys.argv[1:])
    app = make_app(args.config)
    config = Config()
    # 开启 log 线程
    start_thread(log_worker, daemon = True)
    app.run(
        port=args.port or config.server_port,
        )


if __name__ == '__main__':
    main()
