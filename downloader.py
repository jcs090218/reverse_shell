# ========================================================================
# $File: downloader.py $
# $Date: 2019-01-22 16:28:56 $
# $Revision: $
# $Creator: Jen-Chieh Shen $
# $Notice: See LICENSE.txt for modification and distribution information
#                   Copyright © 2019 by Shen, Jen-Chieh $
# ========================================================================

import os
import urllib.request


def download(in_url):
    """Download file by using URL.

    @param { string } in_url : Input url.
    """
    # Get the file name.
    fileName = os.path.join(os.getcwd(), os.path.basename(in_url))
    with urllib.request.urlopen(in_url) as infp:
        with open(fileName, 'wb') as outfp:
            while True:
                data = infp.read(16384)
                if not data:
                    break
                outfp.write(data)
