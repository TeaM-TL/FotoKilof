# -*- coding: utf-8 -*-
# pylint: disable=line-too-long

""" moduł z funkcjami ogólnego przeznaczenia """

import fnmatch
import os
import platform
import re


def spacja(sciezka):
    """ rozwiązanie problemu spacji w nazwach plików i katalogów """

    sciezka = os.path.normpath(sciezka)
    if platform.system() == "Windows":
        czy_spacja = re.search(" ", sciezka)
        if czy_spacja is not None:
            sciezka = '"' + sciezka + '"'
    else:
        sciezka = re.sub(' ', '\ ', sciezka)
        # usuwanie nadmiaru backslashy
        sciezka = re.sub('\\\\\\\\ ', '\ ', sciezka)

    # print("sciezka: ", sciezka)
    return sciezka


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
