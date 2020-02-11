# -*- coding: utf-8 -*-
# pylint: disable=bare-except

"""
module to log writing
- make_log - write into log
"""

import configparser
import datetime
import os

import entries

def write_log(message, level="M", mode="a", initial="0"):
    """
    write message into log file with datestamp
    level: E(rror), W(arning), M(essage)
    mode: a(ppend), w(rite) into log file
    self: to print initial entry into log
    """

    file_ini = os.path.join(os.path.expanduser("~"), ".fotokilof.ini")
    config = configparser.ConfigParser()
    config.read(file_ini, encoding="utf8")
    try:
        log_level = config.get('Konfiguracja', 'log_level')
    except:
        log_level = "M"
    log_level = entries.parse_list(log_level, ("E", "W", "M"), "E")

    # default, write=0 - no logging
    write = 0
    if log_level == "E":
        if level == "E":
            write = 1
    elif log_level == "W":
        if level in ("E", "W"):
            write = 1
    elif log_level == "M":
        write = 1

    if initial == 1:
        write = 1
        mode = "w"
        message = message + " : : " + log_level

    if write == 1:
        logfile = os.path.join(os.path.expanduser("~"), ".fotokilof.log")
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
