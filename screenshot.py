# ========================================================================
# $File: screenshot.py $
# $Date: 2019-01-22 16:37:42 $
# $Revision: $
# $Creator: Jen-Chieh Shen $
# $Notice: See LICENSE.txt for modification and distribution information
#                   Copyright © 2019 by Shen, Jen-Chieh $
# ========================================================================

import datetime
import io
import pyscreenshot


__DEFAULT_SCREENSHOT_FILENAME = "screenshot_"


def pyscreenshot_screenshot():
    """Screenshot the monitor and return image buffer.

    @returns { byte[] } : Image buffer.
    """
    image = pyscreenshot.grab()

    with io.BytesIO() as fp:
        image.save(fp, 'PNG')
        fp.seek(0)
        return fp.read()

def default_screenshot_name():
    """Returns default screenshot name with timestamp."""
    timestamp = f"{datetime.datetime.now():%Y-%m-%d %H_%M_%S}"
    return __DEFAULT_SCREENSHOT_FILENAME + str(timestamp) + ".png"
