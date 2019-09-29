# -*- coding: utf-8 -*-
# pylint: disable=line-too-long

""" moduł z funkcjami ogólnego przeznaczenia """

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

# EOF
