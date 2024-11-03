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
"""

import fnmatch
import logging
from pathlib import PurePosixPath, PureWindowsPath
import os
import os.path

module_logger = logging.getLogger(__name__)


def resize_subdir(resize_vatiant, pixel_x, pixel_y, percent):
    """prepare name for subdir and command for resize"""
    if resize_vatiant == 1:
        command = str(pixel_x) + "x" + str(pixel_y)
        sub_dir = str(pixel_x) + "x" + str(pixel_y)
    elif resize_vatiant == 2:
        if percent > 100:
            percent = 100
        if percent == 0:
            percent = 1
        command = str(percent) + "%"
        sub_dir = str(percent)
    elif resize_vatiant == 3:
        command = "1920x1080"
        sub_dir = "1920x1080"
    elif resize_vatiant == 4:
        command = "2048x1556"
        sub_dir = "2048x1556"
    elif resize_vatiant == 5:
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

    offset_x, offset_y, width, height, gravitation = coordinates

    if gravitation == "NW":
        x0 = offset_x
        y0 = offset_y
        x1 = x0 + width
        y1 = y0 + height
    elif gravitation == "N":
        x0 = x_max / 2 - width / 2
        y0 = offset_y
        x1 = x_max / 2 + width / 2
        y1 = y0 + height
    elif gravitation == "NE":
        x0 = x_max - width - offset_x
        y0 = offset_y
        x1 = x_max - offset_x
        y1 = y0 + height
    elif gravitation == "W":
        x0 = offset_x
        y0 = y_max / 2 - height / 2
        x1 = x0 + width
        y1 = y_max / 2 + height / 2
    elif gravitation == "C":
        x0 = x_max / 2 - width / 2 + offset_x
        y0 = y_max / 2 - height / 2
        x1 = x_max / 2 + width / 2 + offset_x
        y1 = y_max / 2 + height / 2
    elif gravitation == "E":
        x0 = x_max - width - offset_x
        y0 = y_max / 2 - height / 2
        x1 = x_max - offset_x
        y1 = y_max / 2 + height / 2
    elif gravitation == "SW":
        x0 = offset_x
        y0 = y_max - height - offset_y
        x1 = x0 + width
        y1 = y_max - offset_y
    elif gravitation == "S":
        x0 = x_max / 2 - width / 2
        y0 = y_max - height - offset_y
        x1 = x_max / 2 + width / 2
        y1 = y_max - offset_y
    elif gravitation == "SE":
        x0 = x_max - width - offset_x
        y0 = y_max - height - offset_y
        x1 = x_max - offset_x
        y1 = y_max - offset_y
    else:
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
        if request == "first":
            file = file_list[0]
        elif request == "previous":
            if current_file in file_list:
                position = file_list.index(current_file)
                if position > 0:
                    file = file_list[position - 1]
                else:
                    file = None
            else:
                file = file_list[0]
        elif request == "next":
            if current_file in file_list:
                position = file_list.index(current_file)
                if position <= len(file_list) - 2:
                    file = file_list[position + 1]
                else:
                    file = None
            else:
                file = file_list[-1]
        elif request == "last":
            file = file_list[-1]
        else:
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
    if position == "N":
        a = (x0, y0 + length)
        d = (x0 - width, y0 + length_1_3)
        e = (x0 + width, y0 + length_1_3)
        offset_y = length
    elif position == "S":
        a = (x0, y0 - length)
        d = (x0 - width, y0 - length_1_3)
        e = (x0 + width, y0 - length_1_3)
        offset_y = -length
    elif position == "W":
        a = (x0 + length, y0)
        d = (x0 + length_1_3, y0 - width)
        e = (x0 + length_1_3, y0 + width)
        offset_x = length
    elif position == "E":
        a = (x0 - length, y0)
        d = (x0 - length_1_3, y0 - width)
        e = (x0 - length_1_3, y0 + width)
        offset_x = -length
    elif position == "NW":
        a = (x0 + length, y0 + length)
        d = (x0 + length_1_4, y0 + length_1_2)
        e = (x0 + length_1_2, y0 + length_1_4)
        offset_x = length
        offset_y = length
    elif position == "NE":
        a = (x0 - length, y0 + length)
        d = (x0 - length_1_4, y0 + length_1_2)
        e = (x0 - length_1_2, y0 + length_1_4)
        offset_x = -length
        offset_y = length
    elif position == "SE":
        a = (x0 - length, y0 - length)
        d = (x0 - length_1_4, y0 - length_1_2)
        e = (x0 - length_1_2, y0 - length_1_4)
        offset_x = -length
        offset_y = -length
    elif position == "SW":
        a = (x0 + length, y0 - length)
        d = (x0 + length_1_4, y0 - length_1_2)
        e = (x0 + length_1_2, y0 - length_1_4)
        offset_x = length
        offset_y = -length
    else:
        a = (0, 0)
        d = (0, 0)
        e = (0, 0)

    msg = (position, a, c, d, e, offset_x, offset_y)
    module_logger.debug("arrow_gravity: %s", msg)
    return (a, c, d, e, offset_x, offset_y)


def gravitation(gravity, text_x, text_y, image_width, image_height):
    """translate gravitation name from Tk to Pillow specification"""

    if gravity == "NW":
        result0 = "lt"
        result1 = "north_west"
    elif gravity == "N":
        result0 = "mt"
        result1 = "north"
        text_x += image_width / 2
    elif gravity == "NE":
        result0 = "rt"
        result1 = "north_east"
        text_x = image_width - text_x
    elif gravity == "W":
        result0 = "lm"
        result1 = "west"
        text_y += image_height / 2
    elif gravity == "C":
        result0 = "mm"
        result1 = "center"
        text_x += image_width / 2
        text_y += image_height / 2
    elif gravity == "E":
        result0 = "rm"
        result1 = "east"
        text_x = image_width - text_x
        text_y += image_height / 2
    elif gravity == "SW":
        result0 = "lb"
        result1 = "south_west"
        text_y = image_height - text_y
    elif gravity == "S":
        result0 = "mb"
        result1 = "south"
        text_x += image_width / 2
        text_y = image_height - text_y
    elif gravity == "SE":
        result0 = "rb"
        result1 = "south_east"
        text_x = image_width - text_x
        text_y = image_height - text_y
    elif gravity == "0":
        result0 = "0"
        result1 = "0"

    return (result0, result1), text_x, text_y


# EOF
