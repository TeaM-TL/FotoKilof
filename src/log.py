# -*- coding: utf-8 -*-
# pylint: disable=bare-except

"""
Copyright (c) 2019-2021 Tomasz Łuczak, TeaM-TL

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included
in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.

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
            with open(logfile, mode) as log:
                log.write(log_content)
        except:
            print("!make_log: cannot open log file for writing", logfile)
            print(log_content)

# EOF
