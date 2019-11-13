# -*- coding: utf-8 -*-
# pylint: disable=line-too-long

""" moduł z funkcjami ogólnego przeznaczenia """

import fnmatch
import os
import re
from PIL import Image

import mswindows


def humansize(nbytes):
    """ convert size in Byte into human readable: kB, MB, GB
    https://stackoverflow.com/questions/14996453/python-libraries-to-calculate-human-readable-filesize-from-bytes """
    suffixes = ['B', 'KB', 'MB', 'GB', 'TB', 'PB']
    i = 0
    while nbytes >= 1024 and i < len(suffixes)-1:
        nbytes /= 1024.
        i += 1
    value = ('%.2f' % nbytes).rstrip('0').rstrip('.')
    return '%s %s' % (value, suffixes[i])


def mouse_crop_calculation(file, size):
    """ przeliczenie pikseli podglądu  na piksele oryginału """
    # global file_in_path
    img = Image.open(file)
    x_orig = img.size[0]
    y_orig = img.size[1]

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


def spacja(sciezka):
    """ escaping space and special char in pathname """
    if len(sciezka) == 0:
        result = sciezka
    else:
        sciezka = os.path.normpath(sciezka)
        if mswindows.windows() == 1:
            czy_spacja = re.search(" ", sciezka)
            if czy_spacja is not None:
                sciezka = '"' + sciezka + '"'
        else:
            path = os.path.splitext(sciezka)
            path_splitted = path[0].split('/')
            path_escaped = []
            for i in path_splitted:
                path_escaped.append(re.escape(i))
                sciezka = '/'.join(path_escaped) + path[1]
        result = sciezka
    return result

def list_of_images(cwd):
    """
    jpg and png images in cwd
    return sorted list
    """

    list_of_files = os.listdir(cwd)
    file_list = []
    pattern = "*.jpg"
    for file in list_of_files:
        if fnmatch.fnmatch(file, pattern):
            file_list.append(file)
    pattern = "*.png"
    for file in list_of_files:
        if fnmatch.fnmatch(file, pattern):
            file_list.append(file)

    file_list.sort()
    return file_list


def file_from_list_of_images(file_list, current_file, request):
    """return filename from file_list depends of request
    request: position on the list
    """
    if file_list:
        if request == "first":
            file = file_list[0]
        elif request == "previous":
            position = file_list.index(current_file)
            if position > 0:
                file = file_list[position - 1]
            else:
                file = None
        elif request == "next":
            position = file_list.index(current_file)
            if position <= len(file_list) - 2:
                file = file_list[position + 1]
            else:
                file = None
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
