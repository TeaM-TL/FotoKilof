# -*- coding: utf-8 -*-
""" Windows specific module """

import platform


def windows():
    """ checking: system Windows or normal OS """
    if platform.system() == "Windows":
        result = 1
    else:
        result = 0
    return result

# EOF
