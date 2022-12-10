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
- border - add border to picture
- text - add text into picture
- bw - black and white or sepia
- resize - resize picture
- normalize - normalize levels
- contrast - modify contrast
- crop - crop picture

- convert_preview_crop_gravity - convert corrdinates from crop3
- convert_pip - picture in picture, for inserting logo
- gravity - translate eg. NS to Northsouth as Tk expect
- gravity_outside - translate gravitation for adding text outside
"""

import os
from wand.color import Color
from wand.drawing import Drawing
from wand.font import Font
from wand.image import Image
from wand.version import fonts as fontsList
from wand.version import MAGICK_VERSION, VERSION

# my modules
import common
import convert
import magick
import mswindows


def rotate(clone, angle, color, own):
    """ rotate """
    if angle == 0:
        angle = common.empty(own)
        if angle == 0:
            color = None
    else:
        angle = angle
        color = None
    clone.rotate(angle, background=color)


def mirror(file_in, work_dir, extension, flip, flop):
    """ mirror: flip and flop """
    file_out = magick.pre_magick(file_in, work_dir, extension)
    with Image(filename=file_in) as image:
        with image.clone() as clone:
            if flip:
                clone.flip()
            if flop:
                clone.flop()
            
    return file_out


def border(file_in, work_dir, extension, color, x, y):
    """ mirror: flip and flop """
    file_out = magick.pre_magick(file_in, work_dir, extension)
    with Image(filename=file_in) as image:
        with image.clone() as clone:
            clone.border(color, common.empty(x), common.empty(y))
            clone.save(filename=file_out)
    return file_out


def text(file_in, work_dir, extension, 
            in_out, text_color, font, text_size, 
            gravity_onoff, gravity, 
            box, box_color,
            text_x, text_y, text):
    """ add text into picture """

    file_out = magick.pre_magick(file_in, work_dir, extension)
    with Image(filename=file_in) as image:
        with image.clone() as clone:
            if in_out == 0:
            # inside
                with Drawing() as draw:
                    draw.fill_color = text_color
                    draw.font = font
                    draw.font_size = common.empty(text_size)
                    if gravity_onoff == 0:
                        draw.gravity = 'forget'
                    else:
                        draw.gravity = convert.gravity(gravity)
                    if box:
                        draw.text_under_color = box_color
                    draw.text(common.empty(text_x), common.empty(text_y), text)
                    draw(clone)
            else:
                # it has to be fixed
                style = Font(font, common.empty(text_size), text_color)
                clone.font = style
                if box:
                    clone.label(text, gravity=convert.gravity(gravity), background_color=box_color)
                else:
                    clone.label(text, gravity=convert.gravity(gravity))
            clone.save(filename=file_out)
    return file_out


def bw(file_in, work_dir, extension, bw, sepia):
    """ black and white or sepia """
    file_out = magick.pre_magick(file_in, work_dir, extension)
    with Image(filename=file_in) as image:
        with image.clone() as clone:
            if bw == 1:
                # black-white
                clone.type = 'grayscale';
            else:
                # sepia
                clone.sepia_tone(threshold=common.empty(sepia)/100)
            clone.save(filename=file_out)
    return file_out


def resize(file_in, work_dir, extension, resize, pixel, percent, border):
    """ resize picture """

    border = 2 * abs(int(border))
    if resize == 1:
        command = pixel + "x" + pixel
        sub_dir = pixel
    elif resize == 2:
        if percent > 100:
            percent = 100
        if percent == 0:
            percent = 1
        command = str(percent) + "%"
        sub_dir = str(percent)
    elif resize == 3:
        command = str(1920 - border) + "x" + str(1080 - border)
        sub_dir = "1920x1080"
    elif resize == 4:
        command = str(2048 - border) + "x" + str(1556 - border)
        sub_dir = "2048x1556"
    elif resize == 5:
        command = str(4096 - border) + "x" + str(3112 - border)
        sub_dir = "4096x3112"

    file_out = magick.pre_magick(file_in, os.path.join(work_dir, sub_dir), extension)
    with Image(filename=file_in) as image:
        with image.clone() as clone:
            clone.transform(crop='', resize=command)
            clone.save(filename=file_out)

    return file_out


def normalize(file_in, work_dir, extension, normalize, channel):
    """ normalize levels of colors """

    file_out = magick.pre_magick(file_in, work_dir, extension)
    with Image(filename=file_in) as image:
        with image.clone() as clone:
            if normalize == 1:
                if channel != "None":
                    clone.normalize(channel=channel)
                else:
                    clone.normalize()
            elif normalize == 2:
                clone.auto_level()
            clone.save(filename=file_out)

    return file_out


def contrast(file_in, work_dir, extension, selection, contrast, black, white):
    """ normalize levels of colors """

    file_out = magick.pre_magick(file_in, work_dir, extension)
    with Image(filename=file_in) as image:
        with image.clone() as clone:
            if int(selection) == 1:
                    if float(black) > 1:
                        black = 0
                    if float(white) > 1:
                        white = None
                    clone.contrast_stretch(black_point=float(black), white_point=float(white))
            else:
                clone.auto_level()
            clone.save(filename=file_out)

    return file_out


def crop(file_in, work_dir, extension, crop, gravitation, entries):
    """ 
    crop picture 
    entries are as dictionary
    """
    image_size = magick.get_image_size(file_in)
    file_out = magick.pre_magick(file_in, work_dir, extension)
    with Image(filename=file_in) as image:
        with image.clone() as clone:
            if crop == 1:
                if (entries['one_x1'] < entries['one_x2']) and (entries['one_y1'] < entries['one_y2']):
                    if entries['one_x2'] > image_size[0]:
                        entries['one_x2'] = image_size[0]
                    if entries['one_y2'] > image_size[1]:
                        entries['one_y2'] = image_size[1]
                    #print(crop, entries['one_x1'], entries['one_y1'], entries['one_x2'], entries['one_y2'])
                    clone.crop(left=entries['one_x1'], top=entries['one_y1'], 
                            right=entries['one_x2'], bottom=entries['one_y2'])
            if crop == 2:
                if (entries['two_width'] > 0) and (entries['two_height'] > 0):
                    #print(crop, entries['two_x1'], entries['two_y1'], entries['two_width'], entries['two_height'])
                    clone.crop(left=entries['two_x1'], top=entries['two_y1'], 
                                width=entries['two_width'], height=entries['two_height'])
            if crop == 3:
                if (entries['three_width'] > 0) and (entries['three_height'] > 0):
                    #print(crop, entries['three_dx'], entries['three_dy'], entries['three_width'], entries['three_height'], convert.gravity(gravitation))
                    clone.crop(left=entries['three_dx'], top=entries['three_dy'], 
                                width=entries['three_width'], height=entries['three_height'], 
                                gravity=convert.gravity(gravitation))
            clone.save(filename=file_out)

    return file_out

# EOF