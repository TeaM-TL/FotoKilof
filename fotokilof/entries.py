# -*- coding: utf-8 -*-

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

module contains function for parsing GUI entries and INI entries:
- parse_list - validation entry if is on list
- parse_range - validation entry if is in range
- parse_color - validation entry if is a color specification
"""

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

    return result


def parse_range(entry, valid, default):
    """
    parsing entries
    entry - value to check
    default - value if entry is invalid
    valid - valid range
    return - entry or default if entry is out of range
    """

    if valid[0] <= entry <= valid[1]:
        result = entry
    else:
        result = default

    return result


def parse_color(entry, default):
    """
    parsing entries
    entry - value to check
    default - value if entry is invalid
    return - entru or default if entry is out of range
    """
    if re.match('^[#][0-9a-fA-F]{6}$', entry):
        result = entry
    else:
        result = default
    return result

# EOF
