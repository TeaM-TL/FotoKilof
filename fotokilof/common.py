# -*- coding: utf-8 -*-

"""
Copyright (c) 2019-2022 Tomasz Łuczak, TeaM-TL

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
- empty - convert empty string into O, no empty into int
- humansize - converts B to kB or MB
- mouse_crop_calculation - recalculation pixels from previev original image
- spacja - escaping space and special char in pathname
- preview_crop_gravity - convert coordinates for crop3 and logo position
- list_of_images - sorted list images in cwd
- file_from_list_of_images - return filename from file_list depends of request
"""

import fnmatch
import os
import re

import mswindows


def empty(value):
    """ 
    convert empty string into 0 
    non empty into int
    """
    if value == '':
        result = 0
    else:
        result = int(value)
    return result


def humansize(nbytes):
    """
    convert size in Byte into human readable: kB, MB, GB
    https://stackoverflow.com/questions/14996453/python-libraries-to-calculate-human-readable-filesize-from-bytes
    """
    suffixes = ['B', 'KB', 'MB', 'GB', 'TB', 'PB']
    i = 0
    while nbytes >= 1024 and i < len(suffixes)-1:
        nbytes /= 1024.
        i += 1
    value = ('%.2f' % nbytes).rstrip('0').rstrip('.')
    return '%s %s' % (value, suffixes[i])


def mouse_crop_calculation(width, height, size):
    """ recalculation pixels from previev original image """
    x_orig = width
    y_orig = height

    # x_max, y_max - size of preview, we know max: PREVIEW
    if x_orig > y_orig:
        # preview pixels, calculation of y_max preview
        x_max = size
        y_max = x_max*y_orig/x_orig
    elif y_orig > x_orig:
        # calculation of x_max
        y_max = size
        x_max = y_max*x_orig/y_orig
    elif y_orig == x_orig:
        x_max = size
        y_max = size

    dict_return = {}
    dict_return['x_max'] = x_max
    dict_return['y_max'] = y_max
    dict_return['x_orig'] = x_orig
    dict_return['y_orig'] = y_orig
    return dict_return


def spacja(file_path):
    """ escaping space and special char in pathname """
    if len(file_path) == 0:
        result = file_path
    else:
        file_path = os.path.normpath(file_path)
        if mswindows.windows() == 1:
            czy_spacja = re.search(" ", file_path)
            if czy_spacja is not None:
                file_path = '"' + file_path + '"'
        else:
            path = os.path.splitext(file_path)
            path_splitted = path[0].split('/')
            path_escaped = []
            for i in path_splitted:
                path_escaped.append(re.escape(i))
                file_path = '/'.join(path_escaped) + path[1]
        result = file_path
    return result


def preview_crop_gravity(coordinates, x_max, y_max):
    """
    convert corrdinates from crop3:
    offset_x, offset_y, width, height, gravitation
    original image size:
    x_max, y_max
    return coordinates for drawing crop: x0, y0, x1, y1
    """
    offset_x = coordinates[0]
    offset_y = coordinates[1]
    width = coordinates[2]
    height = coordinates[3]
    gravitation = coordinates[4]
    if gravitation == "NW":
        x0 = offset_x
        y0 = offset_y
        x1 = x0 + width
        y1 = y0 + height
    elif gravitation == "N":
        x0 = x_max/2 - width/2
        y0 = offset_y
        x1 = x_max/2 + width/2
        y1 = y0 + height
    elif gravitation == "NE":
        x0 = x_max - width - offset_x
        y0 = offset_y
        x1 = x_max - offset_x
        y1 = y0 + height
    elif gravitation == "W":
        x0 = offset_x
        y0 = y_max/2 - height/2
        x1 = x0 + width
        y1 = y_max/2 + height/2
    elif gravitation == "C":
        x0 = x_max/2 - width/2 + offset_x
        y0 = y_max/2 - height/2 + offset_y
        x1 = x_max/2 + width/2 + offset_x
        y1 = y_max/2 + height/2 + offset_y
    elif gravitation == "E":
        x0 = x_max - width - offset_x
        y0 = y_max/2 - height/2
        x1 = x_max - offset_x
        y1 = y_max/2 + height/2
    elif gravitation == "SW":
        x0 = offset_x
        y0 = y_max - height - offset_y
        x1 = x0 + width
        y1 = y_max - offset_y
    elif gravitation == "S":
        x0 = x_max/2 - width/2
        y0 = y_max - height - offset_y
        x1 = x_max/2 + width/2
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
        y1 = y_max -5
    return (x0, y0, x1, y1)


def list_of_images(cwd):
    """
    jpg, png and tiff images in cwd
    return sorted list
    """

    list_of_files = os.listdir(cwd)
    file_list = []
    patterns = ("*.JPG", "*.JPEG", "*.PNG", "*.TIF", "*.TIFF")
    if mswindows.windows() == 0:
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

# EOF
