# -*- coding: utf-8 -*-
# pylint: disable=bare-except

"""
module to log writing
- make_log - write into log
"""

import configparser
import datetime
import os
from pathlib import Path

import entries

def write_log(message, level="M", mode="a"):
    """
    write message into log file with datestamp
    level: E(rror), W(arning), M(essage)
    mode: a(ppend), w(rite) into log file
    """

    file_ini = os.path.join(str(Path.home()), ".fotokilof.ini")
    config = configparser.ConfigParser()
    config.read(file_ini, encoding="utf8")
    try:
        log_lev = config.get('Konfiguracja', 'log_level')
    except:
        log_lev = "E"
    log_lev = entries.parse_list(log_lev, ("E", "W", "A"), "E")

    # default, 0 - no logging
    write = 0
    if log_lev == "E":
        if level == "E":
            write = 1
    elif log_lev == "W":
        if level in ("E", "W"):
            write = 1
    elif log_lev == "A":
        write = 1

    if write == 1:
        logfile = os.path.join(str(Path.home()), ".fotokilof.log")
        now = str(datetime.datetime.now())
        log_content = now + " :" + level + ": " + message + "\n"
        try:
            log = open(logfile, mode)
            log.write(log_content)
            log.close()
        except:
            print("!make_log: cannot open log file for writing", logfile)
            print(log_content)

# EOF
