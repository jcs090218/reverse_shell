# ========================================================================
# $File: net.py $
# $Date: 2019-01-24 14:11:21 $
# $Revision: $
# $Creator: Jen-Chieh Shen $
# $Notice: See LICENSE.txt for modification and distribution information
#                   Copyright © 2019 by Shen, Jen-Chieh $
# ========================================================================

import socket
import urllib.request


def wan_ip():
    """Returns WAN IP."""
    url = 'http://bot.whatismyipaddress.com'
    ip  = None
    with urllib.request.urlopen(url) as fp:
        ip  = fp.read()
        if isinstance(ip, bytes):
            ip = ip.decode('utf-8')
    return ip

def lan_ip():
    """Returns LAN IP."""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 53))
    ip = s.getsockname()[0]
    s.close()
    return ip
