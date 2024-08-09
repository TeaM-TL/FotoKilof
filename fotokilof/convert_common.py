# -*- coding: utf-8 -*-
# pylint: disable=bare-except

"""
Copyright (c) 2024 Tomasz Łuczak, TeaM-TL

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

Info
- font_list - get list of available fonts
Common
- get_image_size - identify picture: width and height
- display_image - display image
"""

import logging
import os

import PIL.Image
from wand.image import Image
from wand.display import display

import common
import mswindows
import convert_pillow
import convert_wand


def display_image(file_to_display, set_pillow):
    """ display image """
    file_in = common.spacja(file_to_display)
    try:
        if set_pillow or mswindows.windows() or mswindows.macos():
            with PIL.Image.open(file_in) as image:
                image.show()
        else:
            with Image(filename=file_in) as image:
                display(image)
    except:
        logging.error(" Error display file: %s", file_in)
        result = None
    else:
        logging.info(" Display file: %s", file_in)
        result = "OK"

    return result

def get_image_size(file_in, set_pillow):
    """
    identify width and height of picture
    input: file name
    output: size (width, height)
    """

    size = (0, 0)

    if file_in is not None:
        if os.path.isfile(file_in):
            try:
                if set_pillow:
                    with PIL.Image(filename=file_in) as image:
                        size = image.size
                else:
                    with Image(filename=file_in) as image:
                        size = image.size
            except:
                logging.error(" Error read file: %s", file_in)
    return size


def make_clone(file_to_clone, set_pillow, color = None):
    """ open picture and make clone for processing """
    if len(file_to_clone) > 0:
        if set_pillow:
            with PIL.Image(file_to_clone) as image:
                clone = image.copy()
        else:
            with Image(filename=file_to_clone, background=color) as image:
                clone = image.clone()
    else:
        clone = None
    return clone


def save_close_clone(clone, file_out, exif_on, set_pillow):
    if set_pillow:
        convert_pillow.save_close_clone(clone, file_out, exif_on)
    else:
        convert_wand.save_close_clone(clone, file_out, exif_on)


def rotate(clone, rotate, color, rotate_own, set_pillow):
    if set_pillow:
        convert_pillow.rotate(clone, rotate, color, rotate_own)
    else:
        convert_wand.rotate(clone, rotate, color, rotate_own)
