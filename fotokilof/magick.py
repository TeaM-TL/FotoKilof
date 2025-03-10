# -*- coding: utf-8 -*-
# pylint: disable=bare-except

"""
Copyright (c) 2019-2025 Tomasz Łuczak, TeaM-TL

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

module to run ImageMagick:
- magick - picture conversion
"""

import logging
import os

import common

module_logger = logging.getLogger(__name__)


def magick(cmd, file_in, file_out, operating_system):
    """
    run imagemagick command.
    cmd - command for imagemagick
    file_in - fullname picture for processing
    file_out - fullname output picture
    """
    result = None
    if cmd != "":
        if file_in is not None:
            file_in = str(common.spacja(file_in)) + " "
            file_out = " " + str(common.spacja(file_out))
            if operating_system == 'Windows':
                command = "magick.exe "
            else:
                command = "magick "
            command_exec = command + file_in + cmd + file_out
            module_logger.info("Execute: %s", command_exec)
            try:
                os.system(command_exec)
            except:
                module_logger.error("Errot in imagick: %s", command_exec)
                result = None
            else:
                result = "OK"
        else:
            module_logger.warning("imagick: No file for imagick")
            result = None
    else:
        result = None
    return result


# EOF
