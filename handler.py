# ========================================================================
# $File: handler.py $
# $Date: 2019-01-22 22:53:37 $
# $Revision: $
# $Creator: Jen-Chieh Shen $
# $Notice: See LICENSE.txt for modification and distribution information
#                   Copyright © 2019 by Shen, Jen-Chieh $
# ========================================================================

import constant


def encode(msg):
    """Packet encoder."""
    # TODO(jenchieh): Temporary, I surmise.
    return msg.encode(constant.ENCODE_TYPE)

def decode(msg):
    """Package decoder."""
    # TODO(jenchieh): Temporary, I surmise.
    return msg.decode(constant.DECODE_TYPE)
