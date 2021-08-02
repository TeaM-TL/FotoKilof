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

module contains common functions:
- humansize - converts B to kB or MB
- mouse_crop_calculation - recalculation pixels from previev original image
- spacja - escaping space and special char in pathname
- list_of_images - sorted list images in cwd
- file_from_list_of_images - return filename from file_list depends of request
"""

import fnmatch
import os
import re

import magick
import mswindows


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


def mouse_crop_calculation(file_in, size, gm_or_im):
    """ recalculation pixels from previev original image """
    # global file_in_path
    image_size = magick.get_image_size(file_in, gm_or_im)
    x_orig = image_size[0]
    y_orig = image_size[1]

    # x_max, y_max - wymiary podglądu, znamy max czyli PREVIEW
    if x_orig > y_orig:
        # piksele podglądu, trzeba przeliczyć y_max podglądu
        x_max = size
        y_max = x_max*y_orig/x_orig
    elif y_orig > x_orig:
        # przeliczenie x
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


def list_of_images(cwd):
    """
    jpg, png and tiff images in cwd
    return sorted list
    """

    list_of_files = os.listdir(cwd)
    file_list = []
    patterns = ("*.jpg", "*.JPG", "*.jpeg", "*.JPEG", "*.png", "*.PNG", "*.tif", "*.TIF", "*.tiff", "*.TIFF")
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
