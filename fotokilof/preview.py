# -*- coding: utf-8 -*-
# pylint: disable=bare-except

"""
Copyright (c) 2019-2023 Tomasz Łuczak, TeaM-TL

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

module contains function for generating preview and histogram:
- preview_histogram - preview histogram
- preview_wand - for preview pictures
"""

import os
import tempfile

try:
    from wand.drawing import Drawing
except:
    print(" ImageMagick or Wand-py not found")

import common
import convert_wand
import log
import magick
import mswindows

def preview_histogram(file_in):
    """
    histogram generation
    file_in - fullname image file
    dir_temp - fullname temporary directory
    --
    return: fullname of histogram
    """

    if mswindows.windows():
        cmd_magick = "magick.exe convert"
    else:
        cmd_magick = "convert"

    file_histogram = os.path.join(tempfile.gettempdir(), "fotokilof_histogram.ppm")
    command = " -define histogram:unique-colors=false histogram:"
    command = " histogram:"

    magick.magick(command, file_in, file_histogram, cmd_magick)
    try:
        os.system(command)
        return file_histogram
    except:
        log.write_log("Error in convert_histogram: " + command, "E")

    return 'none'


def preview_wand(file_in, size, coord=""):
    """
    preview generation by Wand
    file_in - fullname image file
    size - required size of image
    coord - coordinates for crop
    --
    return:
    - filename - path to PPM file
    - file size
    - width and height
    """

    if file_in is not None:
        if os.path.isfile(file_in):
            filesize = common.humansize(os.path.getsize(file_in))

            clone = convert_wand.make_clone(file_in)
            width = str(clone.width)
            height = str(clone.height)
            clone.convert('ppm')
            convert_wand.resize(clone, str(size) + "x" + str(size))
            

            # write crop if coordinates are given
            if len(coord) == 4 :
                with Drawing() as draw:
                    left_top = (coord[0], coord[1])
                    left_bottom = (coord[0], coord[3])
                    right_top = (coord[2], coord[1])
                    right_bottom = (coord[2], coord[3])
                    draw.fill_color = '#FFFF00'
                    draw.line(left_top, right_top)
                    draw.line(left_top, left_bottom)
                    draw.line(left_bottom, right_bottom)
                    draw.line(right_top, right_bottom)
                    draw(clone)
            preview_width = str(clone.width)
            preview_height = str(clone.height)
            file_preview = os.path.join(tempfile.gettempdir(), "fotokilof_preview.ppm")
            convert_wand.save_close_clone(clone, file_preview)
            result = {'filename': common.spacja(file_preview),
                          'size': filesize,
                          'width': width,
                          'height': height,
                          'preview_width': preview_width,
                          'preview_height': preview_height
                    }
    else:
        result = {'filename': None,
            'size': '0',
            'width': '0',
            'height': '0',
            'preview_width': '0',
            'preview_height': '0'}

    return result

# EOF
