# -*- coding: utf-8 -*-
# pylint: disable=bare-except

"""
Copyright (c) 2022-2023 Tomasz Łuczak, TeaM-TL

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
- make_clone - open origal picture and make clone for processing
- save_close_clone - save clone into file and close clone
- gravitation - translate eg. NS to Northsouth as Wand-py expect
Converters
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
- vignete - add vignete into picture
"""

import os

try:
    from wand.drawing import Drawing
    from wand.image import Image
    from wand.version import fonts as fontsList
    from wand.display import display
except:
    print(" ImageMagick or Wand-py not found")

# my modules
import common
import log


# ------------------------------------ Info
def fonts_list():
    """ list of available fonts """
    return fontsList()


# ------------------------------------ Common
def get_image_size(file_in):
    """
    identify width and height of picture
    input: file name
    output: size (width, height)
    """

    size = (0, 0)

    if file_in is not None:
        if os.path.isfile(file_in):
            try:
                with Image(filename=file_in) as image:
                    size = image.size
            except:
                log.write_log(" Error read file " + file_in, "E")
    return size


def display_image(file_in):
    """ display image """
    file_in = common.spacja(file_in)
    try:
        with Image(filename=file_in) as image:
            display(image)

    except:
        log.write_log(" Error display file: " + file_in, "E")
        result = None
    else:
        log.write_log(" Display file: " + file_in)
        result = "OK"

    return result


def make_clone(file_in, color = None):
    """ open picture and make clone for processing """
    if len(file_in) > 0:
        with Image(filename=file_in, background=color) as image:
            clone = image.clone()
    else:
        clone = None
    return clone


def save_close_clone(clone, file_out, exif = 0):
    """ save and close clone after processing """
    if not exif:
        clone.strip()
    log.write_log(" Save file: " + file_out)
    clone.save(filename=file_out)
    clone.close()


def gravitation(gravity):
    """ translate gravitation name from Tk to Wand-py specification"""

    if gravity == "N":
        result = "north"
    if gravity == "NW":
        result = "north_west"
    if gravity == "NE":
        result = "north_east"
    if gravity == "W":
        result = "west"
    if gravity == "C":
        result = "center"
    if gravity == "E":
        result = "east"
    if gravity == "SW":
        result = "south_west"
    if gravity == "S":
        result = "south"
    if gravity == "SE":
        result = "south_east"
    if gravity == "0":
        result = "0"

    return result


# ------------------------------------ Converters
def pip(clone, logo, logo_data, image_height, image_width):
    """ put picture on picture
    clone - clone of image for processing
    logo - filename of logo
    logo_data = offset_x, offset_y, width, height, gravitation
    original image size: image_height, image_width
    """
    if len(logo):
        with Image(filename=logo) as logo_img:
            with Drawing() as draw:
                position = common.preview_crop_gravity(logo_data, image_height, image_width)
                draw.composite(operator='over',
                                left=common.empty(position[0]),
                                top=common.empty(position[1]),
                                width=common.empty(logo_data[2]),
                                height=common.empty(logo_data[3]),
                                image=logo_img)
                draw(clone)
    log.write_log(" Conversion: logo")


def rotate(clone, angle, color, own):
    """ rotate """
    if angle == 0:
        angle = common.empty(own)
        if angle == 0:
            color = None
    else:
        color = None
    clone.rotate(angle, background=color)
    log.write_log(" Conversion: rotate " + str(angle))


def mirror(clone, flip, flop):
    """ mirror: flip and flop """
    if flip:
        clone.flip()
    if flop:
        clone.flop()
    log.write_log(" Conversion: mirror")


def border(clone, color, x, y):
    """ mirror: flip and flop """
    clone.border(color, common.empty(x), common.empty(y))
    log.write_log(" Conversion: border")


def text(convert_data):
    """ add text into picture """
    clone = convert_data[0]
    in_out = convert_data[1]
    own = convert_data[2]
    angle = convert_data[3]
    text_color = convert_data[4]
    font = convert_data[5]
    text_size = convert_data[6]
    gravity_onoff = convert_data[7]
    gravity = convert_data[8]
    box = convert_data[9]
    box_color = convert_data[10]
    text_x = convert_data[11]
    text_y = convert_data[12]
    text_string = convert_data[13]
    if len(text_string) > 0:
        draw_gravity = gravitation(gravity)
        if in_out == 0:
            # inside
            if gravity_onoff == 0:
                draw_gravity = 'forget'
            if angle == -1:
                angle = common.empty(own)
        else:
            # outside
            if box:
                backgroud_color = box_color
            else:
                backgroud_color = "#FFFFFF"
            angle = 0
            text_x = 0
            text_y = 0

        draw = Drawing()
        if box and not in_out:
            draw.text_under_color = box_color
        draw.fill_color = text_color
        draw.font = font
        draw.font_size = common.empty(text_size)
        draw.gravity = draw_gravity

        if in_out == 0:
            # inside
            clone.annotate(text_string, draw, angle=common.empty(angle),
                    left=common.empty(text_x), baseline=common.empty(text_y))
        else:
            # outside
            metrics = draw.get_font_metrics(clone, text_string, multiline=False)
            with Image(width=clone.width, height=int(metrics.text_height),
                        background=backgroud_color) as canvas:
                canvas.annotate(text_string, draw)
                clone.sequence.append(canvas)
                clone.concat(stacked=True)
    log.write_log(" Conversion: text " + str(in_out))


def bw(clone, bw_variant, sepia):
    """ black and white or sepia """
    if bw_variant == 1:
        # black-white
        clone.type = 'grayscale'
    else:
        # sepia
        clone.sepia_tone(threshold=common.empty(sepia)/100)
    log.write_log(" Conversion: black-white/sepia " + str(bw_variant))


def resize(clone, command):
    """ resize picture """
    clone.transform(crop='', resize=command)
    log.write_log(" Conversion: resize")


def normalize(clone, normalize_variant, channel):
    """ normalize levels of colors """
    if normalize_variant == 1:
        if channel != "None":
            clone.alpha_channel = True
            clone.normalize(channel=channel)
        else:
            clone.normalize()
    else:
        clone.auto_level()
    log.write_log(" Conversion: normalize " + str(normalize_variant))


def contrast(clone, contrast_variant, selection, black, white):
    """ normalize levels of colors """
    if int(contrast_variant) == 1:
        if float(black) > 1:
            black = 0
        if float(white) > 1:
            white = None
        clone.contrast_stretch(black_point=float(black), white_point=float(white))
    else:
        if int(selection) != 0:
            if int(selection) > 0:
                sharpen = True
            else:
                sharpen = False
            iteration = 0
            while iteration < abs(int(selection)):
                iteration += 1
                clone.contrast(sharpen=sharpen)
    log.write_log(" Conversion: contrast " + str(contrast_variant))


def crop(file_in, clone, crop_variant, gravity, entries):
    """
    crop picture
    entries are as dictionary
    """
    image_size = get_image_size(file_in)

    if crop_variant == 1:
        if (entries['one_x1'] < entries['one_x2']) and (entries['one_y1'] < entries['one_y2']):
            if entries['one_x2'] > image_size[0]:
                entries['one_x2'] = image_size[0]
            if entries['one_y2'] > image_size[1]:
                entries['one_y2'] = image_size[1]
            clone.crop(left=entries['one_x1'], top=entries['one_y1'],
                    right=entries['one_x2'], bottom=entries['one_y2'])
    if crop_variant == 2:
        if (entries['two_width'] > 0) and (entries['two_height'] > 0):
            clone.crop(left=entries['two_x1'], top=entries['two_y1'],
                        width=entries['two_width'], height=entries['two_height'])
    if crop_variant == 3:
        if (entries['three_width'] > 0) and (entries['three_height'] > 0):
            clone.crop(left=entries['three_dx'], top=entries['three_dy'],
                        width=entries['three_width'], height=entries['three_height'],
                        gravity=gravitation(gravity))
    log.write_log(" Conversion: crop " + str(crop_variant))


def vignette(clone, dx, dy, radius, sigma):
    """ add vignette into picture
    clone - clone of image for processing
    dx, dy - offset from border
    radius - radius of Gaussian blur
    sigma - standard deviation for Gaussian blur
    color - color of corners
    """
    clone.vignette(radius=common.empty(radius),
                    sigma=common.empty(sigma),
                    x=common.empty(dx),
                    y=common.empty(dy))
    log.write_log(" Conversion: vigette")

# EOF
