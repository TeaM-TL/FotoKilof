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
- display_image - display image
- get_image_size - identify picture: width and height
- preview - preview image
- make_clone
- save_close_clone
- rotate
- mirror
"""

import logging
import time

import PIL

try:
    from wand.image import Image
    from wand.display import display
except:
    print(" ImageMagick or Wand-py not found")

import common
import mswindows
import convert_pillow
import convert_wand


def display_image(file_to_display, set_pillow):
    """display image"""
    file_in = common.spacja(file_to_display)
    # try:
    start_time = time.time()
    if set_pillow or mswindows.windows() or mswindows.macos():
        with PIL.Image.open(file_in) as image:
            image.show()
    else:
        with Image(filename=file_in) as image:
            display(image)
    logging.debug("display_image: %ss", str(time.time() - start_time))
    # except:
    #     logging.error(" Error display file: %s", file_in)
    #     result = None
    # else:
    #     logging.info(" Display file: %s", file_in)
    result = "OK"

    return result


def get_image_size(file_in, set_pillow):
    """
    identify width and height of picture
    input: file name
    output: size (width, height)
    """
    start_time = time.time()
    if set_pillow:
        size = convert_pillow.get_image_size(file_in)
    else:
        size = convert_wand.get_image_size(file_in)
    logging.debug("get_image_size: %ss", str(time.time() - start_time))
    return size


def preview(file_logo, size, set_pillow, coord=""):
    """preview"""
    start_time = time.time()
    if set_pillow:
        result = convert_pillow.preview(file_logo, size, coord)
    else:
        result = convert_wand.preview(file_logo, size, coord)
    logging.debug("preview: %s s", str(time.time() - start_time))
    logging.debug(result)
    return result


def make_clone(file_to_clone, set_pillow, color=None):
    """open picture and make clone for processing"""
    start_time = time.time()
    if set_pillow:
        result = convert_pillow.make_clone(file_to_clone, color)
    else:
        result = convert_wand.make_clone(file_to_clone, color)
    logging.debug("Make clone: %ss", str(time.time() - start_time))
    return result


def save_close_clone(clone, file_out, exif_on, set_pillow):
    """save_close_clone"""
    start_time = time.time()
    if set_pillow:
        convert_pillow.save_close_clone(clone, file_out, exif_on)
    else:
        convert_wand.save_close_clone(clone, file_out, exif_on)
    logging.debug("Save clone: %ss", str(time.time() - start_time))


def rotate(clone, angle, color, angle_own, set_pillow):
    """rotate"""
    start_time = time.time()
    if set_pillow:
        result = convert_pillow.rotate(clone, angle, color, angle_own)
    else:
        convert_wand.rotate(clone, angle, color, angle_own)
        result = clone
    logging.debug("Rotate: %ss", str(time.time() - start_time))
    return result


def mirror(clone, flip, flop, set_pillow):
    """mirror: flip and flop"""
    start_time = time.time()
    if set_pillow:
        result = convert_pillow.mirror(clone, flip, flop)
    else:
        convert_wand.mirror(clone, flip, flop)
        result = clone
    logging.debug("Mirror: %ss", str(time.time() - start_time))
    return result


def resize(clone, command, set_pillow):
    """resize picture"""
    start_time = time.time()
    if set_pillow:
        result = convert_pillow.resize(clone, command)
    else:
        convert_wand.resize(clone, command)
        result = clone
    logging.debug("Resize: %ss", str(time.time() - start_time))
    return result


def border(clone, color, x, y, set_pillow):
    """mirror: flip and flop"""
    start_time = time.time()
    if set_pillow:
        result = convert_pillow.border(clone, color, x, y)
    else:
        convert_wand.border(clone, color, x, y)
        result = clone
    logging.debug("Resize: %ss", str(time.time() - start_time))
    return result
