# ========================================================================
# $File: constant.py $
# $Date: 2019-01-21 23:14:23 $
# $Revision: $
# $Creator: Jen-Chieh Shen $
# $Notice: See LICENSE.txt for modification and distribution information
#                   Copyright © 2019 by Shen, Jen-Chieh $
# ========================================================================


HOST = '127.0.0.1'  # Symbolic name meaning all available interfaces
PORT = 50007        # Arbitrary non-privileged port

# STUDY(jenchieh): Not quite sure how this would effect?
BUF_SIZE = 1024 * 10000

ENCODE_TYPE = 'utf-8'
DECODE_TYPE = 'utf-8'

# Internal command prefix, must be a character.
INTERNAL_CMD_PREFIX = '!'

# Reconnection
RECONNECT_INTERVAL = 60 * 5  # in seconds
