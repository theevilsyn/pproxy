import os
import errno
import sys
import select
import socket
import time
import threading

# from pwn import *

from helpers import *

def main():
    args = parse_args()

    # args.listen_ip = "0.0.0.0"; args.listen_port=1337; args.target_port="1.3.3.7"; args.target_port=1337; args.plugins_out="replace:replace.txt"

    # this is the socket we will listen on for incoming connections
    psocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    psocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    inplugins = None if args.plugins_in is None else generate_plugins(args.plugins_in, incoming=True, verbose=args.verbose)
    outplugins = None if args.plugins_out is None else generate_plugins(args.plugins_out, incoming=False, verbose=args.verbose)

    if(not isValid(args.listen_ip)):
        try:
            args.listen_ip = socket.socket.gethostbyname(args.listen_ip)
        except socket.socket.gaierror:
            print(f"{args.listen_ip} is not a valid IP/hostname")
            sys.exit()

    if(not isValid(args.target_ip)):
        try:
            args.target_ip = socket.socket.gethostbyname(args.target_ip)
        except socket.socket.gaierror:
            print(f"{args.target_ip} is not a valid IP/hostname")
            sys.exit()

    try:
        psocket.bind((args.listen_ip, args.listen_port))
    except socket.error as e:
        print(e.strerror)
        sys.exit(-1)


    psocket.listen(100)
    try:
        while True:
            in_socket, in_addrinfo = psocket.accept()
            proxy_thread = threading.Thread(target=new_proxy,
                                            args=(in_socket, args, inplugins,
                                                    outplugins))
            proxy_thread.start()
    except KeyboardInterrupt:
        print("CTRL+C detected, gracefully stopping the service")


def new_proxy(local_socket, args, inplugins, outplugins):
    remote_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    remote_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    try:
        remote_socket.connect((args.target_ip, args.target_port))
    except socket.error as serror:
        if(serror.errno == errno.ECONNREFUSED):
            print(f'{time.strftime("%Y%m%d-%H%M%S")}, {args.target_ip}:{args.target_port}- Connection refused')
            return None
        elif(serror.errno == errno.ETIMEDOUT):
            print(f'{time.strftime("%Y%m%d-%H%M%S")}, {args.target_ip}:{args.target_port}- Connection timed out')
            return None
        else:
            remote_socket.close(); local_socket.close()
            raise serror
        
    runs = True
    while runs:
        read_sockets, _, _ = select.select([remote_socket, local_socket], [], [])

        for sock in read_sockets:
            try:
                peer = sock.getpeername()
            except socket.error as serror:
                if serror.errno == errno.ENOTCONN:
                    remote_socket.close(); local_socket.close()
                    runs = False
                    break
                else:
                    print(f"{time.strftime('%Y%m%d-%H%M%S')}: Socket exception in new_proxy")
                    raise serror

        data = receive_from(sock)

        if(sock == local_socket):
            if(len(data)):
                # todo logs of outgoing data >>>
                if(outplugins is not None):
                    for plugin in outplugins:
                        data = plugin.execute(data)
                remote_socket.send(data.encode() if isinstance(data, str) else data)
            else:
                print("Connection from local client %s:%d closed" % peer)
                remote_socket.close()
                runs = False
                break
        elif(sock == remote_socket):
            if(len(data)):
                # todo logs of incoming data <<<
                if(inplugins is not None):
                    for plugin in inplugins:
                        data = plugin.execute(data)
                local_socket.send(data.encode()if isinstance(data, str) else data)
            else:
                print("Connection from remote client %s:%d closed" % peer)
                local_socket.close()
                runs = False
                break
        

            
if __name__ == "__main__":
    main()