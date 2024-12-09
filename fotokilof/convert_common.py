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
- fonts_list - fonts list
- display_image - display image
- get_image_size - identify picture: width and height
- preview - preview image
- make_clone
- save_close_clone
- rotate
- mirror
- resize
- border
- nornalize
- bw
- contrast
- crop
- text
- compose
"""

import logging
import os.path
import time
import PIL

try:
    from wand.image import Image
    from wand.display import display

    WAND_TEXT = "Wand found"
except:
    WAND_TEXT = "ImageMagick or Wand-py not found"

import convert_pillow
import convert_wand

import common


module_logger = logging.getLogger(__name__)
module_logger.info(WAND_TEXT)


def fonts_list(set_pillow):
    """list of available fonts"""
    start_time = time.time()
    if set_pillow:
        result = convert_pillow.fonts_list()
    else:
        result = convert_wand.fonts_list()
    module_logger.info("Get fonts list: %ss", str(time.time() - start_time))
    return result


def display_image(file_to_display, set_pillow):
    """display image"""
    # file_in = common.spacja(file_to_display)
    module_logger.info(" Display file: %s", file_to_display)
    start_time = time.time()
    result = None
    if file_to_display:
        if os.path.isfile(file_to_display):
            try:
                if set_pillow:
                    with PIL.Image.open(file_to_display) as image:
                        image.show()
                else:
                    with Image(filename=file_to_display) as image:
                        display(image)
                result = "OK"
            except:
                module_logger.error(
                    "Display_image: Error display file: %s", file_to_display
                )
        else:
            module_logger.error("Display_image: file not found: %s", file_to_display)
    else:
        module_logger.error("Display_image: file is None")
    module_logger.info("Display_image: %ss", str(time.time() - start_time))

    return result


def get_image_size(file_in, is_pillow):
    """
    identify width and height of picture
    input: file name
    output: size (width, height)
    """
    start_time = time.time()
    size = (0, 0)
    if file_in:
        if os.path.isfile(file_in):
            try:
                if is_pillow:
                    with PIL.Image.open(file_in) as image:
                        size = image.size
                else:
                    with Image(filename=file_in) as image:
                        size = image.size
            except:
                module_logger.error("get_image_size: error read file: %s", file_in)
        else:
            module_logger.error("get_image_size: file not found: %s", file_in)
    else:
        module_logger.error("get_image_size: file is None")

    module_logger.info("get_image_size: %ss", str(time.time() - start_time))
    return size


def preview(file_logo, size, set_pillow, operating_system, coord=""):
    """preview"""
    start_time = time.time()
    if set_pillow:
        result = convert_pillow.preview(file_logo, size, operating_system, coord)
    else:
        result = convert_wand.preview(file_logo, size, operating_system, coord)
    module_logger.info("preview: %s s", str(time.time() - start_time))
    return result


def make_clone(file_to_clone, set_pillow, color=None):
    """open picture and make clone for processing"""
    start_time = time.time()
    if set_pillow:
        result = convert_pillow.make_clone(file_to_clone, color)
    else:
        result = convert_wand.make_clone(file_to_clone, color)
    module_logger.info("Make clone: %ss", str(time.time() - start_time))
    return result


def save_close_clone(clone, file_out, exif_on, set_pillow):
    """save_close_clone"""
    if clone:
        start_time = time.time()
        if set_pillow:
            convert_pillow.save_close_clone(clone, file_out, exif_on)
        else:
            convert_wand.save_close_clone(clone, file_out, exif_on)
        module_logger.info("Save clone: %ss", str(time.time() - start_time))


def rotate(clone, angle, color, angle_own, set_pillow):
    """rotate"""
    start_time = time.time()
    if set_pillow:
        result = convert_pillow.rotate(clone, angle, color, angle_own)
    else:
        convert_wand.rotate(clone, angle, color, angle_own)
        result = clone
    module_logger.info("Rotate: %ss", str(time.time() - start_time))
    return result


def mirror(clone, flip, flop, set_pillow):
    """mirror: flip and flop"""
    start_time = time.time()
    if set_pillow:
        result = convert_pillow.mirror(clone, flip, flop)
    else:
        convert_wand.mirror(clone, flip, flop)
        result = clone
    module_logger.info("Mirror: %ss", str(time.time() - start_time))
    return result


def resize(clone, command, set_pillow):
    """resize picture"""
    start_time = time.time()
    if set_pillow:
        result = convert_pillow.resize(clone, command)
    else:
        convert_wand.resize(clone, command)
        result = clone
    module_logger.info("Resize: %ss", str(time.time() - start_time))
    return result


def border(clone, color, x, y, set_pillow):
    """mirror: flip and flop"""
    start_time = time.time()
    if set_pillow:
        result = convert_pillow.border(clone, color, x, y)
    else:
        convert_wand.border(clone, color, x, y)
        result = clone
    module_logger.info("Resize: %ss", str(time.time() - start_time))
    return result


def normalize(clone, normalize_variant, channel, set_pillow):
    """normalize levels of colors"""
    start_time = time.time()
    if set_pillow:
        result = convert_pillow.normalize(clone, normalize_variant, channel)
    else:
        convert_wand.normalize(clone, normalize_variant, channel)
        result = clone
    module_logger.info("Normalize %ss", str(time.time() - start_time))
    return result


def bw(clone, bw_variant, sepia, set_pillow):
    """black and white or sepia"""
    start_time = time.time()
    if set_pillow:
        result = convert_pillow.bw(clone, bw_variant, sepia)
    else:
        convert_wand.bw(clone, bw_variant, sepia)
        result = clone
    module_logger.info("Black-white/sepia %ss", str(time.time() - start_time))
    return result


def contrast(clone, contrast_variant, selection, black, white, set_pillow):
    """black and white or sepia"""
    start_time = time.time()
    if black == "" or black is None:
        black = 0
    if white == "" or white is None:
        white = 0
    if set_pillow:
        result = convert_pillow.contrast(
            clone, contrast_variant, selection, black, white
        )
    else:
        convert_wand.contrast(clone, contrast_variant, selection, black, white)
        result = clone
    module_logger.info("Contrast %ss", str(time.time() - start_time))
    return result


def crop(file_in, clone, crop_variant, gravity, entries, set_pillow):
    """black and white or sepia"""
    image_size = get_image_size(file_in, set_pillow)
    result = None
    match crop_variant:
        case 1:
            if (entries["one_x1"] < entries["one_x2"]) and (
                entries["one_y1"] < entries["one_y2"]
            ):
                if entries["one_x2"] > image_size[0]:
                    entries["one_x2"] = image_size[0]
                if entries["one_y2"] > image_size[1]:
                    entries["one_y2"] = image_size[1]
                left = entries["one_x1"]
                top = entries["one_y1"]
                right = entries["one_x2"]
                bottom = entries["one_y2"]
                result = (left, top, right, bottom)
        case 2:
            if entries["two_width"] and entries["two_height"]:
                left = entries["two_x1"]
                top = entries["two_y1"]
                right = left + entries["two_width"]
                bottom = top + entries["two_height"]
                result = (left, top, right, bottom)
        case 3:
            if entries["three_width"] and entries["three_height"]:
                if set_pillow:
                    result = common.crop_gravity(
                        (
                            entries["three_dx"],
                            entries["three_dy"],
                            entries["three_width"],
                            entries["three_height"],
                            gravity,
                        ),
                        image_size[0],
                        image_size[1],
                    )
                else:
                    gravity_common, text_x, text_y = common.gravitation(
                        gravity, 0, 0, 0, 0
                    )
                    left = entries["three_dx"]
                    top = entries["three_dy"]
                    width = entries["three_width"]
                    height = entries["three_height"]
                    gravity = gravity_common[1]
                    result = (left, top, width, height, gravity)
    if result:
        start_time = time.time()
        if set_pillow:
            result = convert_pillow.crop(clone, result)
        else:
            convert_wand.crop(clone, crop_variant, result)
            result = clone
        module_logger.info("Crop %ss", str(time.time() - start_time))
    else:
        result = clone
    return result


def text(convert_data, set_pillow):
    """black and white or sepia"""
    start_time = time.time()
    if set_pillow:
        result = convert_pillow.text(convert_data)
    else:
        result = convert_wand.text(convert_data)
    module_logger.info("Text %ss", str(time.time() - start_time))
    return result


def compose(clone, compose_file, right, autoresize, color, gravity, set_pillow):
    """join two pictures"""
    if clone:
        start_time = time.time()
        if set_pillow:
            result = convert_pillow.compose(
                clone, compose_file, right, autoresize, color, gravity
            )
        else:
            result = convert_wand.compose(
                clone, compose_file, right, autoresize, color, gravity
            )
        module_logger.info("Compose %ss", str(time.time() - start_time))
        
    else:
        result = None
    return result
