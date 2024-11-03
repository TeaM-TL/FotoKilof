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
import convert_pillow
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


def test_common_gravitation():
    """test pillow gravitation"""
    pos_x, pos_y = (50, 50)
    width, height = (1000, 1000)

    for position in ("N", "S", "E", "W", "NW", "NE", "SW", "SE", "C"):
        if position == "C":
            pos, new_x, new_y = (("mm", "center"), 550, 550)
        elif position == "N":
            pos, new_x, new_y = (("mt", "north"), 550, 50)
        elif position == "S":
            pos, new_x, new_y = (("mb", "south"), 550, 950)
        elif position == "E":
            pos, new_x, new_y = (("rm", "east"), 950, 550)
        elif position == "W":
            pos, new_x, new_y = (("lm", "west"), 50, 550)
        elif position == "NW":
            pos, new_x, new_y = (("lt", "north_west"), 50, 50)
        elif position == "NE":
            pos, new_x, new_y = (("rt", "north_east"), 950, 50)
        elif position == "SW":
            pos, new_x, new_y = (("lb", "south_west"), 50, 950)
        elif position == "SE":
            pos, new_x, new_y = (("rb", "south_east"), 950, 950)

        print(position, pos, new_x, new_y)
        assert common.gravitation(position, pos_x, pos_y, width, height) == (
            pos, new_x, new_y
        )


def test_common_arrow_gravity():
    """test arrow gravity"""
    position = "C"
    length = 40
    dx = 200
    dy = 200

    for position in ("N", "S", "E", "W", "NW", "NE", "SW", "SE"):
        if position == "C":
            a, c, d, e = ((0, 0), (0, 0), (0, 0), (0, 0))
            x = 0
            y = 0
        elif position == "N":
            a, c, d, e, x, y = ((200, 240), (200, 200), (194, 213), (206, 213), 0, 40)
        elif position == "S":
            a, c, d, e, x, y = ((200, 160), (200, 200), (194, 187), (206, 187), 0, -40)
        elif position == "E":
            a, c, d, e, x, y = ((160, 200), (200, 200), (187, 194), (187, 206), -40 , 0)
        elif position == "W":
            a, c, d, e, x, y = ((240, 200), (200, 200), (213, 194), (213, 206), 40, 0)
        elif position == "NW":
            a, c, d, e, x, y = ((240, 240), (200, 200), (210, 220), (220, 210), 40, 40)
        elif position == "NE":
            a, c, d, e, x, y = ((160, 240), (200, 200), (190, 220), (180, 210), -40, 40)
        elif position == "SW":
            a, c, d, e, x, y = ((240, 160), (200, 200), (210, 180), (220, 190), 40, -40)
        elif position == "SE":
            a, c, d, e, x, y = ((160, 160), (200, 200), (190, 180), (180, 190), -40 , -40)

        print(position, a, c, d, e, x, y)
        assert common.arrow_gravity(position, length, dx, dy) == (
            a,
            c,
            d,
            e,
            x,
            y,
        )

