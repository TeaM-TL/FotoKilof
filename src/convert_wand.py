# -*- coding: utf-8 -*-

"""
Copyright (c) 2022 Tomasz Łuczak, TeaM-TL

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

Converters
- rotate - rotate picture
- mirror - mirroring picture
- convert_border - add border to picture

- convert_preview_crop_gravity - convert corrdinates from crop3
- convert_crop - crop picture
- convert_resize - resize picture
- convert_contrast - modify contrast
- convert_normalize - normalize levels
- convert_pip - picture in picture, for inserting logo
- gravity - translate eg. NS to Northsouth as Tk expect
- gravity_outside - translate gravitation for adding text outside
"""

from wand.color import Color
from wand.drawing import Drawing
from wand.font import Font
from wand.image import Image
from wand.version import fonts as fontsList
from wand.version import MAGICK_VERSION, VERSION


# my modules
import common
import magick
import mswindows


def rotate(file_in, work_dir, extension, angle, color):
    """ rotate """
    file_out = magick.pre_magick(file_in, work_dir, extension)
    with Image(filename=file_in) as image:
        with image.clone() as clone:
            clone.rotate(angle, background=color)
            clone.save(filename=file_out)
    return file_out


def mirror(file_in, work_dir, extension, flip, flop):
    """ mirror: flip and flop"""
    file_out = magick.pre_magick(file_in, work_dir, extension)
    with Image(filename=file_in) as image:
        with image.clone() as clone:
            if flip:
                clone.flip()
            if flop:
                clone.flop()
            clone.save(filename=file_out)
    return file_out


def border(file_in, work_dir, extension, color, x, y):
    """ mirror: flip and flop"""
    file_out = magick.pre_magick(file_in, work_dir, extension)
    with Image(filename=file_in) as image:
        with image.clone() as clone:
            clone.border(color, common.empty(x), common.empty(y))
            clone.save(filename=file_out)
    return file_out


def wand():
    """
    convert by oe shot if is possible
    """
    nic = None
