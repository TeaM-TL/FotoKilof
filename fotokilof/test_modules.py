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


def test_common_gravitation():
    """test pillow gravitation"""
    pos_x, pos_y = (50, 50)
    width, height = (1000, 1000)

    for position in ("N", "S", "E", "W", "NW", "NE", "SW", "SE", "C"):
        match position:
            case "C":
                pos, new_x, new_y = (("mm", "center"), 550, 550)
            case "N":
                pos, new_x, new_y = (("mt", "north"), 550, 50)
            case "S":
                pos, new_x, new_y = (("mb", "south"), 550, 950)
            case "E":
                pos, new_x, new_y = (("rm", "east"), 950, 550)
            case "W":
                pos, new_x, new_y = (("lm", "west"), 50, 550)
            case "NW":
                pos, new_x, new_y = (("lt", "north_west"), 50, 50)
            case "NE":
                pos, new_x, new_y = (("rt", "north_east"), 950, 50)
            case "SW":
                pos, new_x, new_y = (("lb", "south_west"), 50, 950)
            case "SE":
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

    for position in ("N", "S", "E", "W", "NW", "NE", "SW", "SE", "C"):
        match position:
            case "C":
                a, c, d, e, x, y = ((240, 240), (200, 200), (210, 220), (220, 210), 40, 60)
            case "N":
                a, c, d, e, x, y = ((200, 240), (200, 200), (194, 213), (206, 213), 0, 40)
            case "S":
                a, c, d, e, x, y = ((200, 160), (200, 200), (194, 187), (206, 187), 0, -40)
            case "E":
                a, c, d, e, x, y = ((160, 200), (200, 200), (187, 194), (187, 206), -40, 0)
            case "W":
                a, c, d, e, x, y = ((240, 200), (200, 200), (213, 194), (213, 206), 40, 0)
            case "NW":
                a, c, d, e, x, y = ((240, 240), (200, 200), (210, 220), (220, 210), 40, 40)
            case "NE":
                a, c, d, e, x, y = ((160, 240), (200, 200), (190, 220), (180, 210), -40, 40)
            case "SW":
                a, c, d, e, x, y = ((240, 160), (200, 200), (210, 180), (220, 190), 40, -40)
            case "SE":
                a, c, d, e, x, y = ((160, 160), (200, 200), (190, 180), (180, 190), -40, -40)

        print(position, a, c, d, e, x, y)
        assert common.arrow_gravity(position, length, dx, dy) == (a, c, d, e, x, y)


def compose_autoresize_canvas(auto_resize, size, compose_x, compose_y, right):
    """calculate canvas for tests"""
    match auto_resize:
        case 0:
            if right:
                canvas_x = size + compose_x
                canvas_y = max(size, compose_y)
            else:
                canvas_x = max(size, compose_x)
                canvas_y = size + compose_y
        case 1:
            if right:
                canvas_x = size + compose_x * size / compose_y
                canvas_y = size
            else:
                canvas_x = size
                canvas_y = size + compose_y * size / compose_x
    return canvas_x, canvas_y
     

def test_compose_calculate_half():
    """test half calculation for compose"""
    compose_x = 1000
    compose_y = 1000
    compose_size = (compose_x, compose_y)
    print("=========== HALF: Compose size: " + str(compose_size))
    gravity = 1
    print("======== Gravity: " + str(gravity))
    for size in (1000, 500, 2000):
        clone = (size, size)
        print("==== Orig size: " + str(clone))
        for autoresize in (1, 0):
            if autoresize:
                resize_factor = size / compose_x
            else:
                resize_factor = 1.0
            canvas_x, canvas_y = compose_autoresize_canvas(autoresize, size, compose_x, compose_y, 1)
            output_data = (0, size, 0, canvas_x, canvas_y, resize_factor)
            print("--- Autoresize: ", autoresize,
                '\n - columns: pos_x1, pos_y1, pos_x2, pos_y2, canvas_x, canvas_y'
                '\n - output',
                output_data)
            print(" - result", common.compose_calculate_half(clone, compose_size, autoresize, gravity))
            assert common.compose_calculate_half(clone, compose_size, autoresize, gravity) == output_data


def test_common_compose_calculation():
    """test compose_calculation"""
    gravity_right = "N"
    gravity_top = "W"
    compose_x = 1000
    compose_y = 2000
    compose_size = (compose_x, compose_y)
    for size in (500, 1000, 2000):
        clone_size = (size, size)
        print("==== FULL: Orig size: " + str(size), "compose size: " + str(compose_size))
        for test in ("right_auto", "right_noauto", "top_auto", "top_noauto"):
            match test:
                case "top_auto":
                    gravity = gravity_top
                    autoresize = 1
                    right = 0
                    resize_factor = size / compose_x
                    canvas_y, canvas_x = compose_autoresize_canvas(autoresize, size, compose_x, compose_y, right)
                    output_data = ((0, 0), (0, size), (int(canvas_y), int(canvas_x)), resize_factor)
                case "right_auto":
                    gravity = gravity_right
                    autoresize = 1
                    right = 1
                    resize_factor = size / compose_y
                    canvas_x, canvas_y = compose_autoresize_canvas(autoresize, size, compose_x, compose_y, right)
                    output_data = ((0, 0), (size, 0), (int(canvas_x), int(canvas_y)), resize_factor)
                case "top_noauto":
                    gravity = gravity_top
                    autoresize = 0
                    right = 0
                    resize_factor = 1.0
                    canvas_x, canvas_y = compose_autoresize_canvas(autoresize, size, compose_x, compose_y, right)
                    output_data = ((0, 0), (0, size), (int(canvas_x), int(canvas_y)), resize_factor)
                case "right_noauto":
                    gravity = gravity_right
                    autoresize = 0
                    right = 1
                    resize_factor = 1.0
                    canvas_x, canvas_y = compose_autoresize_canvas(autoresize, size, compose_x, compose_y, right)
                    output_data = ((0, 0), (size, 0), (int(canvas_x), int(canvas_y)), resize_factor)
            print("--- " + test, clone_size, compose_size, right, autoresize,
                        '\n - columns: position_1, position_2, canvas'
                        '\n - output',
                        output_data)
            print(" - result", common.compose_calculation(clone_size, compose_size, autoresize, right, gravity))
            assert common.compose_calculation(clone_size, compose_size, autoresize, right, gravity) == output_data
