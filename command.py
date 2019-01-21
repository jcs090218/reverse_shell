# ========================================================================
# $File: command.py $
# $Date: 2019-01-21 23:06:02 $
# $Revision: $
# $Creator: Jen-Chieh Shen $
# $Notice: See LICENSE.txt for modification and distribution information
#                   Copyright © 2019 by Shen, Jen-Chieh $
# ========================================================================

import enum


class Command(enum.Enum):
    """List of command type."""

    # Halt
    EXIT = "exit"
    SHUTDOWN = "shutdown"

    # Listen
    SCREENSHOT = "screenshot"

    # Download
    DOWNLOAD = "dwn"
