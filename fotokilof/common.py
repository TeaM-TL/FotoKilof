# -*- coding: utf-8 -*-

"""
Copyright (c) 2019-2024 Tomasz Łuczak, TeaM-TL

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

module contains common functions:
- resize_subdir - calculation of directory name and converion argument for resize
- empty - convert empty string into O, no empty into int
- humansize - converts B to kB or MB
- mouse_crop_calculation - recalculation pixels from previev original image
- spacja - escaping space and special char in pathname
- crop_gravity - convert coordinates for crop3 and logo position
- list_of_images - sorted list images in cwd
- file_from_list_of_images - return filename from file_list depends of request
- arrow_gravity - calculate coordinates if draw arrow
- gravitation - translate eg. NS to Northsouth or lt as Wand-py or Pillow expect
- compose_calculate_half - calculate compose for one domension for compose_calculation
- compose_calculation - calculation position for compose
"""

import fnmatch
import logging
from pathlib import PurePosixPath, PureWindowsPath
import os
import os.path

module_logger = logging.getLogger(__name__)


def resize_subdir(resize_vatiant, pixel_x, pixel_y, percent):
    """prepare name for subdir and command for resize"""
    match resize_vatiant:
        case 1:
            command = str(pixel_x) + "x" + str(pixel_y)
            sub_dir = str(pixel_x) + "x" + str(pixel_y)
        case 2:
            if percent > 100:
                percent = 100
            if percent == 0:
                percent = 1
            command = str(percent) + "%"
            sub_dir = str(percent)
        case 3:
            command = "1920x1080"
            sub_dir = "1920x1080"
        case 4:
            command = "2048x1556"
            sub_dir = "2048x1556"
        case 5:
            command = "4096x3112"
            sub_dir = "4096x3112"
    return (sub_dir, command)


def empty(value):
    """
    convert empty string into 0
    non empty into int
    """
    if value == "":
        result = 0
    else:
        result = int(value)
    return result


def humansize(nbytes):
    """
    convert size in Byte into human readable: kB, MB, GB
    https://stackoverflow.com/questions/14996453/python-libraries-to-calculate-human-readable-filesize-from-bytes
    """
    suffixes = ["B", "kB", "MB", "GB", "TB", "PB"]
    i = 0
    while nbytes >= 1024 and i < len(suffixes) - 1:
        nbytes /= 1024.0
        i += 1
    value = ("%.2f" % nbytes).rstrip("0").rstrip(".")
    return "%s %s" % (value, suffixes[i])


def mouse_crop_calculation(x_orig, y_orig, size):
    """recalculation pixels from previev original image"""

    # x_max, y_max - size of preview, we know max: PREVIEW
    if x_orig > y_orig:
        # preview pixels, calculation of y_max preview
        x_max = size
        y_max = x_max * y_orig / x_orig
    elif y_orig > x_orig:
        # calculation of x_max
        y_max = size
        x_max = y_max * x_orig / y_orig
    elif y_orig == x_orig:
        x_max = size
        y_max = size

    dict_return = {}
    dict_return["x_max"] = x_max
    dict_return["y_max"] = y_max
    dict_return["x_orig"] = x_orig
    dict_return["y_orig"] = y_orig
    return dict_return


def spacja(file_path, operating_system):
    """escaping space and special char in pathname"""
    if len(file_path):
        if operating_system == "Windows":
            result = PureWindowsPath(os.path.normpath(file_path))
        else:
            result = PurePosixPath(os.path.normpath(file_path))
    else:
        result = None
    return result


def crop_gravity(coordinates, x_max, y_max):
    """
    convert corrdinates from crop3:
    offset_x, offset_y, width, height, gravitation
    original image size:
    x_max, y_max
    return coordinates for drawing crop: x0, y0, x1, y1
    """

    offset_x, offset_y, width, height, gravite = coordinates

    match gravite:
        case "NW":
            x0 = offset_x
            y0 = offset_y
            x1 = x0 + width
            y1 = y0 + height
        case "N":
            x0 = x_max / 2 - width / 2
            y0 = offset_y
            x1 = x_max / 2 + width / 2
            y1 = y0 + height
        case "NE":
            x0 = x_max - width - offset_x
            y0 = offset_y
            x1 = x_max - offset_x
            y1 = y0 + height
        case "W":
            x0 = offset_x
            y0 = y_max / 2 - height / 2
            x1 = x0 + width
            y1 = y_max / 2 + height / 2
        case "C":
            x0 = x_max / 2 - width / 2 + offset_x
            y0 = y_max / 2 - height / 2
            x1 = x_max / 2 + width / 2 + offset_x
            y1 = y_max / 2 + height / 2
        case "E":
            x0 = x_max - width - offset_x
            y0 = y_max / 2 - height / 2
            x1 = x_max - offset_x
            y1 = y_max / 2 + height / 2
        case "SW":
            x0 = offset_x
            y0 = y_max - height - offset_y
            x1 = x0 + width
            y1 = y_max - offset_y
        case "S":
            x0 = x_max / 2 - width / 2
            y0 = y_max - height - offset_y
            x1 = x_max / 2 + width / 2
            y1 = y_max - offset_y
        case "SE":
            x0 = x_max - width - offset_x
            y0 = y_max - height - offset_y
            x1 = x_max - offset_x
            y1 = y_max - offset_y
        case _:
            x0 = 5
            y0 = 5
            x1 = x_max - 5
            y1 = y_max - 5
    return (x0, y0, x1, y1)


def list_of_images(cwd, operating_system):
    """
    jpg, png and tiff images in cwd
    return sorted list
    """

    list_of_files = os.listdir(cwd)
    file_list = []
    patterns = ("*.JPG", "*.JPEG", "*.PNG", "*.TIF", "*.TIFF")
    if operating_system != "Windows":
        patterns = patterns + ("*.jpg", "*.jpeg", "*.png", "*.tif", "*.tiff")

    for pattern in patterns:
        for file in list_of_files:
            if fnmatch.fnmatch(file, pattern):
                file_list.append(file)

    file_list.sort()
    return file_list


def file_from_list_of_images(file_list, current_file, request):
    """
    return filename from file_list depends of request
    request: position on the list
    """
    if file_list:
        match request:
            case "first":
                file = file_list[0]
            case "previous":
                if current_file in file_list:
                    position = file_list.index(current_file)
                    if position > 0:
                        file = file_list[position - 1]
                    else:
                        file = None
                else:
                    file = file_list[0]
            case "next":
                if current_file in file_list:
                    position = file_list.index(current_file)
                    if position <= len(file_list) - 2:
                        file = file_list[position + 1]
                    else:
                        file = None
                else:
                    file = file_list[-1]
            case "last":
                file = file_list[-1]
            case _:
                file = None
    else:
        file = None

    if file == current_file:
        file = None
    return file


def arrow_gravity(position, length, x0, y0):
    """calculate coordinated to draw arrow"""
    length = int(length)
    x0 = int(x0)
    y0 = int(y0)
    width = int(length / 3 / 2)
    length_1_2 = int(length / 2)
    length_1_3 = int(length / 3)
    length_1_4 = int(length / 4)

    offset_x = 0
    offset_y = 0
    c = (x0, y0)
    a = (x0, y0)
    d = (x0, y0)
    e = (x0, y0)
    match position:
        case "N":
            a = (x0, y0 + length)
            d = (x0 - width, y0 + length_1_3)
            e = (x0 + width, y0 + length_1_3)
            offset_y = length
        case "S":
            a = (x0, y0 - length)
            d = (x0 - width, y0 - length_1_3)
            e = (x0 + width, y0 - length_1_3)
            offset_y = -length
        case "W":
            a = (x0 + length, y0)
            d = (x0 + length_1_3, y0 - width)
            e = (x0 + length_1_3, y0 + width)
            offset_x = length
        case "E":
            a = (x0 - length, y0)
            d = (x0 - length_1_3, y0 - width)
            e = (x0 - length_1_3, y0 + width)
            offset_x = -length
        case "NW":
            a = (x0 + length, y0 + length)
            d = (x0 + length_1_4, y0 + length_1_2)
            e = (x0 + length_1_2, y0 + length_1_4)
            offset_x = length
            offset_y = length
        case "NE":
            a = (x0 - length, y0 + length)
            d = (x0 - length_1_4, y0 + length_1_2)
            e = (x0 - length_1_2, y0 + length_1_4)
            offset_x = -length
            offset_y = length
        case "SE":
            a = (x0 - length, y0 - length)
            d = (x0 - length_1_4, y0 - length_1_2)
            e = (x0 - length_1_2, y0 - length_1_4)
            offset_x = -length
            offset_y = -length
        case "SW":
            a = (x0 + length, y0 - length)
            d = (x0 + length_1_4, y0 - length_1_2)
            e = (x0 + length_1_2, y0 - length_1_4)
            offset_x = length
            offset_y = -length
        case "C":
            a = (x0 + length, y0 + length)
            d = (x0 + length_1_4, y0 + length_1_2)
            e = (x0 + length_1_2, y0 + length_1_4)
            offset_x = length
            offset_y = 1.5 * length

    msg = (position, a, c, d, e, offset_x, offset_y)
    module_logger.debug("arrow_gravity: %s", msg)
    return (a, c, d, e, offset_x, offset_y)


def gravitation(gravity, text_x, text_y, image_width, image_height):
    """translate gravitation name from Tk to Pillow specification"""

    match gravity:
        case "NW":
            result0 = "lt"
            result1 = "north_west"
        case "N":
            result0 = "mt"
            result1 = "north"
            text_x += image_width / 2
        case "NE":
            result0 = "rt"
            result1 = "north_east"
            text_x = image_width - text_x
        case "W":
            result0 = "lm"
            result1 = "west"
            text_y += image_height / 2
        case "C":
            result0 = "mm"
            result1 = "center"
            text_x += image_width / 2
            text_y += image_height / 2
        case "E":
            result0 = "rm"
            result1 = "east"
            text_x = image_width - text_x
            text_y += image_height / 2
        case "SW":
            result0 = "lb"
            result1 = "south_west"
            text_y = image_height - text_y
        case "S":
            result0 = "mb"
            result1 = "south"
            text_x += image_width / 2
            text_y = image_height - text_y
        case "SE":
            result0 = "rb"
            result1 = "south_east"
            text_x = image_width - text_x
            text_y = image_height - text_y
        case "0":
            result0 = "0"
            result1 = "0"
        case _:
            result0 = "0"
            result1 = "0"

    return (result0, result1), text_x, text_y


def compose_calculate_half(clone, compose, auto_resize, gravity):
    """
    calculate compose for one size
    if right use x1=x1, y1=y1 etc.
    if top use x1=y1, xy=x1 etc.
    """
    clone_w, clone_h = clone
    compose_x, compose_y = compose

    pos_x2 = clone_w

    # default
    pos_y1 = 0
    pos_y2 = 0

    if auto_resize:
        resize_factor = clone_h / compose_y
        canvas_x = clone_w + compose_x * resize_factor
        canvas_y = clone_h
    else:
        resize_factor = 1
        canvas_x = clone_w + compose_x
        canvas_y = max(clone_h, compose_y)
        if clone_h > compose_y:
            match gravity:
                case 1:
                    pass
                case 3:
                    pos_y2 = int(canvas_y - compose_y)
                case _:
                    pos_y2 = int((canvas_y - compose_y) / 2)
        elif clone_h < compose_y:
            match gravity:
                case 1:
                    pos_y1 = 0
                case 3:
                    pos_y1 = int(canvas_y - clone_h)
                case _:
                    pos_y1 = int((canvas_y - clone_h) / 2)
        else:
            canvas_y = clone_h

    return pos_y1, pos_x2, pos_y2, canvas_x, canvas_y, resize_factor


def compose_calculation(clone_size, compose_size, autoresize, right, gravity):
    """calculation position for compose"""

    clone_width, clone_height = clone_size
    compose_width, compose_height = compose_size
    if right:
        match gravity:
            case "N":
                gravity = 1
            case "S":
                gravity = 3
            case _:
                gravity = 2
        pos_y1, pos_x2, pos_y2, canvas_width, canvas_height, resize_factor = (
            compose_calculate_half(
                (clone_width, clone_height),
                (compose_width, compose_height),
                autoresize,
                gravity,
            )
        )
    else:
        match gravity:
            case "W":
                gravity = 1
            case "E":
                gravity = 3
            case _:
                gravity = 2
        pos_y1, pos_y2, pos_x2, canvas_height, canvas_width, resize_factor = (
            compose_calculate_half(
                (clone_height, clone_width),
                (compose_height, compose_width),
                autoresize,
                gravity,
            )
        )
    return (
        (0, int(pos_y1)),
        (int(pos_x2), int(pos_y2)),
        (int(canvas_width), int(canvas_height)),
        resize_factor,
    )


# EOF
