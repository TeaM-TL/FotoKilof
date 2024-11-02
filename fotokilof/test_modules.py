# -*- coding: utf-8 -*-

"""
Copyright (c) 2024 Tomasz Łuczak, TeaM-TL

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
"""

import check_new_version
import common
import gui
import version


def test_check_version():
    """tests for check_new_version"""
    assert check_new_version.check_version(version.__version__)[0] == 0


def test_gui_only_numbers():
    """test only numbers"""
    assert gui.only_numbers("1")
    # assert gui.only_numbers('a')


def test_gui_only_integer():
    """test only integer"""
    assert gui.only_integer(1)


def test_common_empty():
    """test empty"""
    assert common.empty("") == 0
    assert common.empty("11") == 11


def test_common_humansize():
    """test humansize"""
    assert common.humansize(100) == "100 B"
    assert common.humansize(2048) == "2 kB"


def test_common_crop_gravity():
    """test crom_gravity
    coordinates = (offset_x, offset_y, width, height, gravitation)
    """
    coordinates = (0, 0, 100, 100, "SE")
    assert common.crop_gravity(coordinates, 1000, 500) == (900, 400, 1000, 500)
