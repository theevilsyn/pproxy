import sys
import argparse

def isValid(ip):
    octets = ip.split(".")
    return False if len(octets)!=4 else True

def parse_args():
    parser = argparse.ArgumentParser(description='Simple proxy servie for data ' +
                                                 'interception and ' +
                                                 'modification. ' +
                                                 'Select plugins to handle ' +
                                                 'the intercepted traffic.')

    parser.add_argument('-ti', '--targetip', dest='target_ip',
                        help='remote target IP or host name')

    parser.add_argument('-tp', '--targetport', dest='target_port', type=int,
                        help='remote target port')

    parser.add_argument('-li', '--listenip', dest='listen_ip',
                        default='0.0.0.0', help='IP address/host name to listen for ' +
                        'incoming data')

    parser.add_argument('-lp', '--listenport', dest='listen_port', type=int,
                        default=1337, help='port to listen on')

    parser.add_argument('-pi', '--pluginsin', dest='plugins_in',
                        help='comma-separated list of plugins to modify data' +
                             ' received from the remote target.')

    parser.add_argument('-po', '--pluginsout', dest='plugins_out',
                        help='comma-separated list of plugins to modify data' +
                             ' before sending to remote target.')

    parser.add_argument('-v', '--verbose', dest='verbose', default=False,
                        action='store_true',
                        help='More verbose output of status information')

    return parser.parse_args()

# ./proxy.py -ti 1.1.1.1 -tp 1111 -lp 0.0.0.0 -lp 1337 -po replace:file=sample.txt:file2=sample2.txt,hexdump,http


def receive_from(sock): # receive data from a socket until no more data is there
    b = b""
    while True:
        data = sock.recv(4096)
        b += data
        if not data or len(data) < 4096:
            break
    return b

def parse_options(meh):
    mehh = meh.split(":", 1)
    if len(mehh) == 1: # no options present
        return mehh[0], None

    name = mehh[0]
    ops = mehh[1].split(":")
    options = {}
    for op in ops:
        try:
            k,v = op.split("=")
            options[k] = v
        except ValueError:
            print(f"{op} is not valid!!")
            sys.exit()
    return name, options

def generate_plugins(plugins, incoming, verbose=False):
    pluglist = []
    for plugin in plugins.split(","):
        name, options = parse_options(plugin)
        try:
            __import__(f"plugins.{name}")
            pluglist.append(sys.modules[f"plugins.{name}"].Plugin(incoming, options, verbose))
        except ImportError:
            print(f"Plugin {name} not found!")
            sys.exit()

    return pluglist

