# -*- coding: utf-8 -*-
# pylint: disable=bare-except

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

module contains function for generating preview and histogram:
- preview_histogram
- preview_convert - preview by ImageMagick - used for logo
- preview_pillow - preview by Pillow - faster - used for preview original and result
"""

import os
import tempfile
from PIL import Image, ImageDraw

import common
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


def preview_convert(file_in, command, size, gm_or_im):
    """
    preview generation
    file_in - fullname image file
    command - additional command for imagemagick or space
    dir_temp - fullname temporary directory
    --
    return:
    - filename - path to PPM file
    - file size
    - width and height
    """
    try:
        image = Image.open(file_in)
        width, height = image.size
        filesize = common.humansize(os.path.getsize(file_in))

        cmd_magick = gm_or_im + "convert"
        command = " -resize " + str(size) + "x" + str(size) + command
        file_preview = os.path.join(tempfile.gettempdir(),
                                    "fotokilof_" + os.getlogin() \
                                    + "_preview.ppm")
        magick.magick(command, file_in, file_preview, cmd_magick)

        result = {'filename': file_preview, 'size': filesize, \
                'width': str(width), 'height': str(height)}
    except:
        log.write_log("Error in preview_convert: return", "E")
        result = None

    return result


def preview_pillow(file_in, size, coord):
    """
    preview generation
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

            try:
                image = Image.open(file_in)
                width = image.width
                height = image.height
                if width > height:
                    width_resize = int(size)
                    height_resize = int(height / width * size )
                elif width < height:
                    height_resize = int(size)
                    width_resize = int(width / height * size )
                else:
                    width_resize = int(size)
                    height_resize = int(size)
            except:
                log.write_log("Error in preview_pillow: image width and height", "E")
                result = None

            try:
                image_resized = image.resize((width_resize, height_resize))
                if len(coord) == 4 :
                    draw = ImageDraw.Draw(image_resized)
                    left_up = (coord[0],coord[1])
                    left_dn = (coord[0], coord[3])
                    right_up = (coord[2],coord[1])
                    right_dn = (coord[2], coord[3])
                    draw.line([left_up, left_dn, right_dn, right_up, left_up], fill=128)
            except:
                log.write_log("Error in preview_pillow: resize and draw", "E")
                result = None

            try:
                if image.mode != 'RGB':
                    image = image.convert('RGB')

                file_preview = os.path.join(tempfile.gettempdir(),
                                            "fotokilof_" + os.getlogin() \
                                            + "_preview.ppm")
                image_resized.save(file_preview, "PPM")

                result = {'filename': file_preview,
                          'size': filesize,
                          'width': str(width),
                          'height': str(height)}
            except:
                log.write_log("Error in preview_pillow: make preview", "E")
                result = None
        else:
            result = None
    else:
        result = None

    return result

# EOF
