# -*- coding: utf-8 -*-
# pylint: disable=bare-except

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

module to work with ImageMagick:
- magick - picture conversion
- magick_command - make ImageMagick independent
"""

import os
import re
import shutil

import common
import log
import mswindows


def magick(cmd, file_in, file_out, command):
    """
    run imagemagick command.
    cmd - command for imagemagick
    file_in - fullname picture for processing
    file_out - fullname output picture
    command:
      convert, mogrify, composite, import - ImageMagick
      gm convert, gm mogrify, gm composite, gm import - GraphicsMagick
    """
    result = None
    if cmd != "":
        if file_in is not None:
            file_in = common.spacja(file_in)
            file_out = common.spacja(file_out)
            command = magick_command(command)
            command = command + " " + file_in  + " " + cmd + file_out
            log.write_log("Execute: " + command, "M")
            try:
                os.system(command)
            except:
                log.write_log("Errot in imagick: " + command, "E")
                result = None
            else:
                result = "OK"
        else:
            log.write_log("imagick: No file for imagick", "W")
            result = None
    else:
        result = None
    return result


def magick_command(command):
    """
    make ImageMagick independent
    command: it depends:
      - Unix: convert, mogrify, composite
      - Windows: magick.exe convert, magick.exe mogrify, magick.exe composite
    """
    if mswindows.windows() == 1:
        suffix = ".exe "
    else:
        suffix = " "
    tool = command.split()
    tool.insert(1, suffix)
    tool.extend(' ')
    result = "".join(tool)
    return result


# EOF
