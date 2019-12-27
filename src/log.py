# -*- coding: utf-8 -*-

"""
module to log writing
- make_log - write into log
"""

import datetime
import os
from pathlib import Path


def write_log(message, mode="a"):
    """
    write message into log file with datestamp
    """

    logfile = os.path.join(str(Path.home()), ".fotokilof.log")
    now = str(datetime.datetime.now())
    log_content = now + " : " + message + "\n"
    try:
        log = open(logfile, mode)
        log.write(log_content)
        log.close()
    except:
        print("!make_log: cannot open log file for writing", logfile)
        print("!log: ", now + " : : " +  message)

# EOF
