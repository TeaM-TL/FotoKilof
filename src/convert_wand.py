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
- font_list - get list of available fonts
- magick_wand_version - info about versions of IM ag Wand
- make_clone - open origal picture and make clone for processing
- save_close_clone - save clone into file and close clone
- pip - picture in picture, for inserting logo
- rotate - rotate picture
- mirror - mirroring picture
- border - add border to picture
- text - add text into picture
- bw - black and white or sepia
- resize - resize picture
- normalize - normalize levels
- contrast - modify contrast
- crop - crop picture
"""

from wand.color import Color
from wand.drawing import Drawing
from wand.font import Font
from wand.image import Image, COMPOSITE_OPERATORS
from wand.version import fonts as fontsList
from wand.version import MAGICK_VERSION, VERSION

# my modules
import common
import convert
import magick


def fonts_list():
    """ list of available fonts """
    return fontsList()


def magick_wand_version():
    """ version of ImageMagick and Wand-py """
    return 'IM:' + MAGICK_VERSION.split(' ')[1] + ' : Wand:' + VERSION


def make_clone(file_in):
    """ open picture and make clone for processing """
    with Image(filename=file_in) as image:
        clone = image.clone()
        return clone

def save_close_clone(clone, file_out):
    """ save and close clone after processing """
    clone.save(filename=file_out) 
    clone.close()


def pip(clone, logo, width, height, offset_dx, offset_dy):
    """ put picture on picture """
    if len(logo):
        with Image(filename=logo) as logo:
            with Drawing() as draw:
                draw.composite(operator='over', left=common.empty(offset_dx), top=common.empty(offset_dy),
                                width=common.empty(width), height=common.empty(height), image=logo)
                draw(clone)


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


def mirror(clone, flip, flop):
    """ mirror: flip and flop """
    if flip:
        clone.flip()
    if flop:
        clone.flop()


def border(clone, color, x, y):
    """ mirror: flip and flop """
    clone.border(color, common.empty(x), common.empty(y))


def text(clone, in_out, 
            text_color, font, text_size, 
            gravity_onoff, gravity, 
            box, box_color,
            text_x, text_y, text):
    """ add text into picture """
    if len(text) > 0:
        if in_out == 0:
        # inside
            with Drawing() as draw:
                draw.fill_color = text_color
                draw.font = font
                draw.font_size = common.empty(text_size)
                if gravity_onoff == 0:
                    draw.gravity = 'forget'
                else:
                    draw.gravity = str(convert.gravitation(gravity))
                if box:
                    draw.text_under_color = box_color
                draw.text(common.empty(text_x), common.empty(text_y), text)
                draw(clone)
        else:
            # it has to be fixed
            style = Font(font, common.empty(text_size), text_color)
            clone.font = style
            if box:
                clone.label(text, gravity=convert.gravitation(gravity), background_color=box_color)
            else:
                clone.label(text, gravity=convert.gravitation(gravity))


def bw(clone, bw, sepia):
    """ black and white or sepia """
    if bw == 1:
        # black-white
        clone.type = 'grayscale';
    else:
        # sepia
        clone.sepia_tone(threshold=common.empty(sepia)/100)


def resize_subdir(resize, pixel, percent):
    """ prepare name for subdir and command for resize """
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
        command = '1920x1080'
        sub_dir = "1920x1080"
    elif resize == 4:
        command = "2048x1556"
        sub_dir = "2048x1556"
    elif resize == 5:
        command = "4096x3112"
        sub_dir = "4096x3112"
    return (sub_dir, command)

    
def resize(clone, command):
    """ resize picture """
    clone.transform(crop='', resize=command)


def normalize(clone, normalize, channel):
    """ normalize levels of colors """
    if normalize == 1:
        if channel != "None":
            clone.normalize(channel=channel)
        else:
            clone.normalize()
    elif normalize == 2:
        clone.auto_level()


def contrast(clone, selection, contrast, black, white):
    """ normalize levels of colors """
    if int(selection) == 1:
            if float(black) > 1:
                black = 0
            if float(white) > 1:
                white = None
            clone.contrast_stretch(black_point=float(black), white_point=float(white))
    else:
        clone.auto_level()


def crop(file_in, clone, crop, gravity, entries):
    """ 
    crop picture 
    entries are as dictionary
    """
    image_size = magick.get_image_size(file_in)

    if crop == 1:
        if (entries['one_x1'] < entries['one_x2']) and (entries['one_y1'] < entries['one_y2']):
            if entries['one_x2'] > image_size[0]:
                entries['one_x2'] = image_size[0]
            if entries['one_y2'] > image_size[1]:
                entries['one_y2'] = image_size[1]
            clone.crop(left=entries['one_x1'], top=entries['one_y1'], 
                    right=entries['one_x2'], bottom=entries['one_y2'])
    if crop == 2:
        if (entries['two_width'] > 0) and (entries['two_height'] > 0):
            clone.crop(left=entries['two_x1'], top=entries['two_y1'], 
                        width=entries['two_width'], height=entries['two_height'])
    if crop == 3:
        if (entries['three_width'] > 0) and (entries['three_height'] > 0):
            clone.crop(left=entries['three_dx'], top=entries['three_dy'], 
                        width=entries['three_width'], height=entries['three_height'], 
                        gravity=convert.gravitation(gravity))
            

# EOF