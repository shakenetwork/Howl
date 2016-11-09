import argparse
import os


def main(logfile, target, port):
    if os.path.exists(logfile):
        print('The file is exists! overwirte it? (y/n)')
        check = input()
        if check == 'y':
            os.system('rm {}'.format(logfile))
        else:
            return
    os.system("whatweb --no-errors -t 255 {} --url-suffix=':{}' --log-json={}".format(target, port, logfile))
    print('ok')
if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='howl')
    parser.add_argument('-f', help='log file', default='/tmp/whatweb_tmp.json')
    parser.add_argument('-t', help='target')
    parser.add_argument('-p', help='http port', default='80')
    args = parser.parse_args()
    logfile = args.f
    target = args.t
    port = args.p
    main(logfile, target, port)
