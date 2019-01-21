# ========================================================================
# $File: logger.py $
# $Date: 2019-01-21 23:38:22 $
# $Revision: $
# $Creator: Jen-Chieh Shen $
# $Notice: See LICENSE.txt for modification and distribution information
#                   Copyright © 2019 by Shen, Jen-Chieh $
# ========================================================================

import datetime


def info(in_str):
    """Log info."""
    __log("INFO", in_str)

def warning(in_str):
    """Log warning."""
    __log("WARNING", in_str)

def error(in_str):
    """Log error."""
    __log("ERROR", in_str)


def __log(in_title, in_str):
    """Log template.

    @param { typename } in_title : Title of the message.
    @param { typename } in_str : Log content.
    """
    timestamp = datetime.datetime.now()

    print(f"* [{in_title}] ({timestamp}) {in_str} ")
