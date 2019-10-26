# -*- coding: utf-8 -*-
# pylint: disable=line-too-long

"""  module contains function for parsing GUI entries and INI entries """


def parse_list(entry, valid, default):
    """
    parsing entries
    entry - value to check
    valid - valid range
    return - entru or default if entry is out of range
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
    valid - valid range
    return - entru or default if entry is out of range
    """
    if entry >= valid[0] and entry <= valid[1]:
        result = entry
    else:
        result = default

    print(entry, valid, default, result)
    return result


def parse_color(entry, valid, default):
    """
    parsing entries
    entry - value to check
    valid - valid range
    return - entru or default if entry is out of range
    """
    if entry >= valid[0] and entry <= valid[1]:
        result = entry
    else:
        result = default
    print(entry, valid, default, result)
    return result

# EOF
