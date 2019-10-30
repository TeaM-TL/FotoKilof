# -*- coding: utf-8 -*-
# pylint: disable=line-too-long

"""  module contains function for parsing GUI entries and INI entries """

import re

def parse_list(entry, valid, default):
    """
    parsing entries
    entry - value to check
    valid - valid range
    default - value if entry is invalid
    return - entry or default if entry is out of range
    """
    if entry in valid:
        result = entry
    else:
        result = default

    # print(entry, valid, default, result)
    return result


def parse_range(entry, valid, default):
    """
    parsing entries
    entry - value to check
    default - value if entry is invalid
    valid - valid range
    return - entru or default if entry is out of range
    """
    if entry >= valid[0] and entry <= valid[1]:
        result = entry
    else:
        result = default

    print(entry, valid, default, result)
    return result


def parse_color(entry, default):
    """
    parsing entries
    entry - value to check
    default - value if entry is invalid
    return - entru or default if entry is out of range
    """
    if re.match('^[#][0-9A-F]{6}$', entry):
        result = entry
    else:
        result = default
    return result

# EOF
