# ========================================================================
# $File: command.py $
# $Date: 2019-01-21 23:06:02 $
# $Revision: $
# $Creator: Jen-Chieh Shen $
# $Notice: See LICENSE.txt for modification and distribution information
#                   Copyright © 2019 by Shen, Jen-Chieh $
# ========================================================================

import enum

import constant


class Command(enum.Enum):
    """List of command type."""

    # Halt
    EXIT = "exit"
    SHUTDOWN = "shutdown"

    # Listen
    SCREENSHOT = "screenshot"

    # Download
    DOWNLOAD = "dl"


def get_cmd_params(full_cmd):
    """Get the command and all parameters.

    @param { string } full_cmd : Full command string.
    """
    parts = full_cmd.split(" ")

    cmd = parts[0]
    params = parts[1:]

    return (cmd, params)


def is_internal_command(full_cmd):
    """Check if the `full_cmd' the internal command.

    @param { string } full_cmd : Target command to check.
    """
    for it in Command:
        if it.value == full_cmd:
            return True
    return False

def is_internal_command_prefix(full_cmd):
    """Check if the current command the internal command.

    @param { string } full_cmd : Input command.
    """
    return full_cmd[:1] == constant.INTERNAL_CMD_PREFIX
