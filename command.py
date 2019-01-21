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
    DOWNLOAD = "dwn"


def is_internal_command(in_cmd):
    """Check if the current command the internal command.

    @param { string } in_cmd : Input command.
    """
    return in_cmd[:1] == constant.INTERNAL_CMD_PREFIX
