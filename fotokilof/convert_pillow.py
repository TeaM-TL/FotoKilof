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
- compose - join two pictures
"""

import logging
import tempfile
import os
from PIL import Image, ImageOps

# my modules
import common


# ------------------------------------ Info
def version():
    """version of PIL"""
    return Image.__version__


def fonts_list():
    """list of available fonts"""
    return fontsList()


# ------------------------------------ Common
def make_clone(file_to_clone, color=None):
    """open picture and make clone for processing"""
    if len(file_to_clone) > 0:
        with Image.open(file_to_clone) as image:
            clone = image.copy()
    else:
        clone = None
    return clone


def save_close_clone(clone, file_out, ppm=0, exif=0):
    """save and close clone after processing"""
    # if not exif:
    #     clone.strip()
    logging.info(" Save file: %s", file_out)
    clone.save(file_out)
    clone.close()


def get_image_size(filename):
    """
    identify width and height of picture
    input: file name
    output: size (width, height)
    """
    size = (0, 0)
    if filename is not None:
        if os.path.isfile(filename):
            try:
                with Image.open(filename) as image:
                    size = image.size
            except:
                logging.error(" Error read file: %s", filename)
    logging.debug("get_image_size: %s, %s", filename, str(size))
    return size


def gravitation(gravity):
    """translate gravitation name from Tk to Wand-py specification"""

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
    """put picture on picture
    clone - clone of image for processing
    logo - filename of logo
    logo_data = offset_x, offset_y, width, height, gravitation
    original image size: image_height, image_width
    """
    if len(logo):
        with Image(filename=logo) as logo_img:
            with Drawing() as draw:
                position = common.preview_crop_gravity(
                    logo_data, image_height, image_width
                )
                draw.composite(
                    operator="over",
                    left=common.empty(position[0]),
                    top=common.empty(position[1]),
                    width=common.empty(logo_data[2]),
                    height=common.empty(logo_data[3]),
                    image=logo_img,
                )
                draw(clone)
    logging.info(" Conversion: logo")


def rotate(clone, angle, color, own):
    """rotate"""
    if angle == 0:
        angle = common.empty(own)
        if angle == 0:
            color = None
    else:
        color = None
    if angle == 90:
        result = clone.transpose(Image.Transpose.ROTATE_90)
    elif angle == 180:
        result = clone.transpose(Image.Transpose.ROTATE_180)
    elif angle == 270:
        result = clone.transpose(Image.Transpose.ROTATE_270)
    else:
        result = clone
        logging.debug("rotate: only 90 180 and 270, %s not allowed", str(angle))
    # clone.rotate(angle)
    logging.info(" Conversion: rotate %s", str(angle))
    return result


def mirror(clone, flip, flop):
    """mirror: flip and flop"""
    result = clone
    if flip:
        # result = clone.transpose(Image.Transpose.FLIP_TOP_BOTTOM)
        result = ImageOps.flip(clone)
    if flop:
        # result = result.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
        result = ImageOps.mirror(result)
    logging.info(" Conversion: mirror")
    return result


def border(clone, color, x, y):
    """border: color, x, y"""
    result = ImageOps.expand(clone, (int(x), int(y)), color)
    logging.info("Conversion: border")
    return result


def text(convert_data):
    """add text into picture"""
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
                draw_gravity = "forget"
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
            clone.annotate(
                text_string,
                draw,
                angle=common.empty(angle),
                left=common.empty(text_x),
                baseline=common.empty(text_y),
            )
        else:
            # outside
            metrics = draw.get_font_metrics(clone, text_string, multiline=False)
            with Image(
                width=clone.width,
                height=int(metrics.text_height),
                background=backgroud_color,
            ) as canvas:
                canvas.annotate(text_string, draw)
                clone.sequence.append(canvas)
                clone.concat(stacked=True)
    logging.info(" Conversion: text %s", str(in_out))


def bw(clone, bw_variant, sepia):
    """black and white or sepia"""
    if bw_variant == 1:
        # black-white
        result = ImageOps.grayscale(clone)
    else:
        print("not ready yet")
        # sepia
        # clone.sepia_tone(threshold=common.empty(sepia) / 100)
    logging.info(" Conversion: black-white/sepia %s", str(bw_variant))
    return result


def resize(clone, size):
    """resize picture"""
    image_width, image_height = clone.size

    if "x" in size:
        width, height = size.split("x")
        if int(width) > int(height):
            max_size = int(width)
        else:
            max_size = int(height)

        if image_width > image_height:
            final_width, final_height = (
                max_size,
                int(image_height * (max_size / image_width)),
            )
        elif image_width < image_height:
            final_width, final_height = (
                int(image_width * (max_size / image_height)),
                max_size,
            )
        else:
            final_width, final_height = (max_size, max_size)
    else:
        max_size = int(size.split("%")[0])
        final_width = max_size * image_width / 100
        final_height = max_size * image_height / 100

    result = clone.resize((int(final_width), int(final_height)))
    logging.info(" Conversion: resize")
    return result


def normalize(clone, normalize_variant, channel):
    """normalize levels of colors"""
    if normalize_variant == 1:
        result = ImageOps.autocontrast(clone)
        # if channel != "None":
        #     clone.alpha_channel = True
        #     clone.normalize(channel=channel)
        # else:
        #     clone.normalize()
    else:
        result = ImageOps.equalize(clone)
    logging.info(" Conversion: normalize %s", str(normalize_variant))
    return result


def contrast(clone, contrast_variant, selection, black, white):
    """normalize levels of colors"""
    result = None
    if int(contrast_variant) == 1:
        if float(black) > 100:
            black = 100
        if float(white) > 100:
            white = 100
        # clone.contrast_stretch(black_point=float(black), white_point=float(white))
        result = ImageOps.autocontrast(clone, (float(black), float(white)))
    # else:
    #     if int(selection) != 0:
    #         if int(selection) > 0:
    #             sharpen = True
    #         else:
    #             sharpen = False
    #         iteration = 0
    #         while iteration < abs(int(selection)):
    #             iteration += 1
    #             clone.contrast(sharpen=sharpen)
    logging.info(" Conversion: contrast %s", str(contrast_variant))
    return result


def crop(file_in, clone, crop_variant, gravity, entries):
    """
    crop picture
    entries are as dictionary
    """
    image_size = get_image_size(file_in)

    if crop_variant == 1:
        if (entries["one_x1"] < entries["one_x2"]) and (
            entries["one_y1"] < entries["one_y2"]
        ):
            if entries["one_x2"] > image_size[0]:
                entries["one_x2"] = image_size[0]
            if entries["one_y2"] > image_size[1]:
                entries["one_y2"] = image_size[1]
            clone.crop(
                left=entries["one_x1"],
                top=entries["one_y1"],
                right=entries["one_x2"],
                bottom=entries["one_y2"],
            )
    if crop_variant == 2:
        if (entries["two_width"] > 0) and (entries["two_height"] > 0):
            clone.crop(
                left=entries["two_x1"],
                top=entries["two_y1"],
                width=entries["two_width"],
                height=entries["two_height"],
            )
    if crop_variant == 3:
        if (entries["three_width"] > 0) and (entries["three_height"] > 0):
            clone.crop(
                left=entries["three_dx"],
                top=entries["three_dy"],
                width=entries["three_width"],
                height=entries["three_height"],
                gravity=gravitation(gravity),
            )
    logging.info(" Conversion: crop %s", str(crop_variant))


def vignette(clone, dx, dy, radius, sigma):
    """add vignette into picture
    clone - clone of image for processing
    dx, dy - offset from border
    radius - radius of Gaussian blur
    sigma - standard deviation for Gaussian blur
    color - color of corners
    """
    clone.vignette(
        radius=common.empty(radius),
        sigma=common.empty(sigma),
        x=common.empty(dx),
        y=common.empty(dy),
    )
    logging.info(" Conversion: vigette")


def compose(clone, compose_file, right, autoresize, color, gravity):
    """join two pictures
    clone - clone of image for processing
    compose_file - file to join
    right - join on right or bottom side
    autoresize - autoresize picture or not
    color - color to fill gap if no autoresize
    gravity - position if no autoresize
    """
    if len(compose_file):
        with Image(filename=compose_file) as compose_image:
            if right:
                stacked = False
                # for canvas
                canvas_width = clone.width + compose_image.width
                if clone.height >= compose_image.height:
                    canvas_height = clone.height
                else:
                    canvas_height = compose_image.height
                # for autoresize
                resize_width = compose_image.width * clone.height / compose_image.height
                resize_height = clone.height
                # for no autoresize
                position_x1 = 0
                position_x2 = clone.width
                if clone.height >= compose_image.height:
                    # orig > compose
                    position_y1 = 0
                    if gravity == "N":
                        position_y2 = 0
                    elif gravity == "S":
                        position_y2 = canvas_height - compose_image.height
                    else:
                        position_y2 = canvas_height / 2 - compose_image.height / 2
                else:
                    # orig < compose
                    position_y2 = 0
                    if gravity == "N":
                        position_y1 = 0
                    elif gravity == "S":
                        position_y1 = canvas_height - clone.height
                    else:
                        position_y1 = canvas_height / 2 - clone.height / 2
            else:
                stacked = True
                # for canvas
                if clone.width >= compose_image.width:
                    canvas_width = clone.width
                else:
                    canvas_width = compose_image.width
                canvas_height = clone.height + compose_image.height
                # for autoresize
                resize_width = clone.width
                resize_height = compose_image.height * clone.width / compose_image.width
                # for no autoresize
                position_y1 = 0
                position_y2 = clone.height
                if clone.width >= compose_image.width:
                    # orig > compose
                    position_x1 = 0
                    if gravity == "W":
                        position_x2 = 0
                    elif gravity == "E":
                        position_x2 = canvas_width - compose_image.width
                    else:
                        position_x2 = canvas_width / 2 - compose_image.width / 2
                else:
                    # orig < compose
                    position_x2 = 0
                    if gravity == "W":
                        position_x1 = 0
                    elif gravity == "E":
                        position_x1 = canvas_width - clone.width
                    else:
                        position_x1 = canvas_width / 2 - clone.width / 2

            if autoresize:
                # autoresize, no problem
                resize_value = str(resize_width) + "x" + str(resize_height)
                compose_image.transform(crop="", resize=resize_value)
                clone.sequence.append(compose_image)
                clone.concat(stacked=stacked)
            else:
                # no autoresize
                with Image(
                    width=canvas_width, height=canvas_height, background=color
                ) as canvas:
                    with Drawing() as draw:
                        # original picture
                        draw.composite(
                            operator="over",
                            left=position_x1,
                            top=position_y1,
                            width=clone.width,
                            height=clone.height,
                            image=clone,
                        )
                        draw(canvas)
                        # picture to join
                        draw.composite(
                            operator="over",
                            left=position_x2,
                            top=position_y2,
                            width=compose_image.width,
                            height=compose_image.height,
                            image=compose_image,
                        )
                        draw(canvas)
                    clone.image_set(canvas)

    logging.info(" Conversion: compose")


# ------------------------------------ Preview
def preview(file_in, max_size, coord=""):
    """
    preview generation by Wand
    file_in - fullname image file
    max_size - required size of image
    coord - coordinates for crop
    --
    return:
    - filename - path to PPM file
    - file size
    - width and height
    """

    result = {
        "filename": None,
        "size": "0",
        "width": "0",
        "height": "0",
        "preview_width": "0",
        "preview_height": "0",
    }

    if file_in is not None:
        if os.path.isfile(file_in):
            filesize = common.humansize(os.path.getsize(file_in))
            clone = make_clone(file_in)
            width, height = clone.size
            if width > height:
                preview_width, preview_height = (
                    max_size,
                    int(height * (max_size / width)),
                )
            elif width < height:
                preview_width, preview_height = (
                    int(width * (max_size / height)),
                    max_size,
                )
            else:
                preview_width, preview_height = (max_size, max_size)
            size = (preview_width, preview_height)
            clone = clone.resize(size)
            # write crop if coordinates are given
            if len(coord) == 4:
                with Drawing() as draw:
                    left_top = (coord[0], coord[1])
                    left_bottom = (coord[0], coord[3])
                    right_top = (coord[2], coord[1])
                    right_bottom = (coord[2], coord[3])
                    draw.fill_color = "#FFFF00"
                    draw.line(left_top, right_top)
                    draw.line(left_top, left_bottom)
                    draw.line(left_bottom, right_bottom)
                    draw.line(right_top, right_bottom)
                    draw(clone)
            preview_width, preview_height = clone.size
            file_preview = os.path.join(tempfile.gettempdir(), "fotokilof_preview.ppm")
            save_close_clone(clone, file_preview)
            result = {
                "filename": common.spacja(file_preview),
                "size": filesize,
                "width": str(width),
                "height": str(height),
                "preview_width": str(preview_width),
                "preview_height": str(preview_height),
            }
            logging.debug("preview: %s", str(result))
    return result


# EOF
