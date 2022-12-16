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

module contains function for generating preview and histogram:
- preview_histogram - preview histogram
- preview_wand - for preview pictures 
"""

import os
import tempfile
from wand.drawing import Drawing
from wand.image import Image

import common
import convert_wand
import log
import magick


def preview_histogram(file_in, gm_or_im):
    """
    histogram generation
    file_in - fullname image file
    dir_temp - fullname temporary directory
    --
    return: fullname of histogram
    """

    cmd_magick = gm_or_im + "convert"
    file_histogram = os.path.join(tempfile.gettempdir(),
                                  "fotokilof_" + os.getlogin() \
                                  + "_histogram.ppm")
    command = " -define histogram:unique-colors=false histogram:"
    command = " histogram:"

    magick.magick(command, file_in, file_histogram, cmd_magick)
    try:
        os.system(command)
        return file_histogram
    except:
        log.write_log("Error in convert_histogram: " + command, "E")

    return 'none'


def preview_wand(file_in, size, coord):
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
            width = clone.width
            height = clone.height

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
            clone.convert('ppm')
            file_preview = os.path.join(tempfile.gettempdir(),
                                            "fotokilof_" + os.getlogin() \
                                            + "_preview.ppm")
            convert_wand.save_close_clone(clone, file_preview, 0)
            result = {'filename': file_preview,
                          'size': filesize,
                          'width': str(width),
                          'height': str(height)}
            return result

# EOF
