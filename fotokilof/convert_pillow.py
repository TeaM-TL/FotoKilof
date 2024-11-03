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
- fonts_list - get list of available fonts
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
- preview - preview done by Pillow
"""

import logging
import tempfile
import os
import os.path
from PIL import Image, ImageDraw, ImageOps, ImageFont

from find_system_fonts_filename import (
    get_system_fonts_filename,
    FindSystemFontsFilenameException,
)

# my modules
import common

module_logger = logging.getLogger(__name__)


# ------------------------------------ Info
def version():
    """version of PIL"""
    return Image.__version__


def fonts_list():
    """list of available fonts"""
    try:
        fonts_filename = get_system_fonts_filename()
        module_logger.debug("Get fonts list from system")
    except FindSystemFontsFilenameException:
        # Deal with the exception
        module_logger.error("Errort to get fonts list from system")
        fonts_filename = None
    if fonts_filename is not None:
        result = []
        for item in fonts_filename:
            result.append(item)
        result.sort()
    else:
        result = "Arial"
    return result


# ------------------------------------ Common
def make_clone(file_to_clone, color=None):
    """open picture and make clone for processing"""
    if len(file_to_clone) > 0:
        with Image.open(file_to_clone) as image:
            result = image.copy()
    else:
        result = None
    return result


def save_close_clone(clone, file_out, ppm=0, exif=0):
    """save and close clone after processing"""
    if clone is None:
        module_logger.error(" Clone for %s is None", file_out)
    else:
        # if not exif:
        #     clone.strip()
        module_logger.debug(" Save file: %s", file_out)
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
                module_logger.error(" Error read file: %s", filename)
    module_logger.debug("get_image_size: %s, %s", filename, str(size))
    return size


def gravitation(gravity):
    """translate gravitation name from Tk to Pillow specification"""

    if gravity == "N":
        result = "ma"
    if gravity == "NW":
        result = "la"
    if gravity == "NE":
        result = "ra"
    if gravity == "W":
        result = "lm"
    if gravity == "C":
        result = "mm"
    if gravity == "E":
        result = "rm"
    if gravity == "SW":
        result = "ld"
    if gravity == "S":
        result = "ld"
    if gravity == "SE":
        result = "rd"
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
                position = common.crop_gravity(logo_data, image_height, image_width)
                draw.composite(
                    operator="over",
                    left=common.empty(position[0]),
                    top=common.empty(position[1]),
                    width=common.empty(logo_data[2]),
                    height=common.empty(logo_data[3]),
                    image=logo_img,
                )
                draw(clone)
    module_logger.debug(" Conversion: logo")


def rotate(clone, angle, color, own):
    """rotate"""
    if angle == 0:
        angle = common.empty(own)
        if angle == 0:
            color = None
    else:
        color = None
    result = clone.rotate(angle=angle, fillcolor=color, expand=True)
    module_logger.debug(" Conversion: rotate %s", str(angle))
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
    module_logger.debug(" Conversion: mirror")
    return result


def border(clone, color, x, y):
    """border: color, x, y"""
    result = ImageOps.expand(clone, (int(x), int(y)), color)
    module_logger.debug("Conversion: border")
    return result


def text(convert_data):
    """add text into picture"""
    clone = convert_data[0]
    in_out = convert_data[1]
    own = convert_data[2]
    angle = convert_data[3]
    angle = 0
    text_color = convert_data[4]
    font = convert_data[5]
    text_size = int(convert_data[6])
    gravity_onoff = convert_data[7]
    gravity = convert_data[8]
    box = convert_data[9]
    box = 0
    box_color = convert_data[10]
    text_x = int(common.empty(convert_data[11]))
    text_y = int(common.empty(convert_data[12]))
    text_string = convert_data[13]
    # arrow = convert_data[14]
    arrow = 1

    image_width, image_height = clone.size
    font = ImageFont.truetype(font, text_size)

    if len(text_string):
        if in_out == 0:
            # inside
            if gravity_onoff == 0:
                draw_gravity = "lt"
            else:
                if gravity == "NW":
                    draw_gravity = "lt"
                elif gravity == "N":
                    draw_gravity = "mt"
                    text_x += image_width / 2
                elif gravity == "NE":
                    draw_gravity = "rt"
                    text_x = image_width - text_x
                elif gravity == "W":
                    draw_gravity = "lm"
                    text_y += image_height / 2
                elif gravity == "C":
                    draw_gravity = "mm"
                    text_x += image_width / 2
                    text_y += image_height / 2
                elif gravity == "E":
                    draw_gravity = "rm"
                    text_x = image_width - text_x
                    text_y += image_height / 2
                elif gravity == "SW":
                    draw_gravity = "lb"
                    text_y = image_height - text_y
                elif gravity == "S":
                    draw_gravity = "mb"
                    text_x += image_width / 2
                    text_y = image_height - text_y
                elif gravity == "SE":
                    draw_gravity = "rb"
                    text_x = image_width - text_x
                    text_y = image_height - text_y
            draw_text = ImageDraw.Draw(clone)
            if arrow:
                if gravity_onoff == 0:
                    gravity = "NW"
                a, c, d, e, offset_x, offset_y = common.arrow_gravity(gravity, text_size, text_x, text_y)
                if gravity != "C":
                    draw_text.line([a, c], fill=text_color, width=2)
                    draw_text.line([d, c], fill=text_color, width=2)
                    draw_text.line([e, c], fill=text_color, width=2)
            else:
                offset_x = 0
                offset_y = 0
            draw_text.text(
                (text_x + offset_x, text_y + offset_y),
                text_string,
                fill=text_color,
                font=font,
                anchor=draw_gravity,
            )
            result = clone
            module_logger.debug(" Conversion: text inside")
        else:
            # outside
            left, top, right, bottom = font.getbbox(text_string)
            if gravity == "W":
                text_x = 0
                draw_gravity = "lt"
            elif gravity == "C":
                text_x = image_width / 2
                draw_gravity = "mt"
            elif gravity == "E":
                text_x = image_width
                draw_gravity = "rt"
            else:
                text_x = 0
                draw_gravity = "lt"
            image_text = Image.new("RGB", (image_width, bottom), box_color)
            draw_outside_text = ImageDraw.Draw(image_text)
            draw_outside_text.text(
                (text_x, top / 2),
                text_string,
                fill=text_color,
                font=font,
                anchor=draw_gravity,
            )
            image_outside = Image.new("RGB", (image_width, image_height + bottom))
            image_outside.paste(clone)
            image_outside.paste(image_text, (0, image_height))
            result = image_outside
            module_logger.debug(" Conversion: text outside")

        module_logger.debug(" Conversion: text")
    return result


def bw(clone, bw_variant, sepia):
    """black and white or sepia"""
    if bw_variant == 1:
        # black-white
        result = ImageOps.grayscale(clone)
    else:
        module_logger.warning(
            "Black-white/sepia not available for PILLOW, install ImageMagick"
        )
        # sepia
        # clone.sepia_tone(threshold=common.empty(sepia) / 100)
    module_logger.debug(" Conversion: black-white/sepia %s", str(bw_variant))
    return result


def resize(clone, size):
    """resize picture"""
    image_width, image_height = clone.size
    if "x" in size:
        width, height = size.split("x")
        width = int(width)
        height = int(height)

        if width > height:
            max_size = width
        else:
            max_size = height

        ratio = 1
        if width > height:
            final_width, final_height = (
                max_size,
                int(image_height * (max_size / image_width)),
            )
            if final_height > height:
                ratio = height / final_height
        elif width < height:
            final_width, final_height = (
                int(image_width * (max_size / image_height)),
                max_size,
            )
            if final_width > width:
                ratio = width / final_width
        else:
            final_width, final_height = (max_size, max_size)
        final_width = int(final_width * ratio)
        final_height = int(final_height * ratio)
    else:
        max_size = int(size.split("%")[0])
        final_width = max_size * image_width / 100
        final_height = max_size * image_height / 100

    result = clone.resize((int(final_width), int(final_height)))
    module_logger.debug(
        " Conversion: resize %s x %s", str(final_width), str(final_height)
    )
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
    module_logger.debug(" Conversion: normalize %s", str(normalize_variant))
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
    module_logger.debug(" Conversion: contrast %s", str(contrast_variant))
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
            left = entries["one_x1"]
            top = entries["one_y1"]
            right = entries["one_x2"]
            bottom = entries["one_y2"]
            result = clone.crop((left, top, right, bottom))
    if crop_variant == 2:
        if (entries["two_width"] > 0) and (entries["two_height"] > 0):
            left = entries["two_x1"]
            top = entries["two_y1"]
            right = left + entries["two_width"]
            bottom = top + entries["two_height"]
            result = clone.crop((left, top, right, bottom))
    if crop_variant == 3:
        if (entries["three_width"] > 0) and (entries["three_height"] > 0):
            clone = clone.crop(
                common.crop_gravity(
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
            )
        result = clone
    module_logger.debug(" Conversion: crop %s", str(crop_variant))
    return result


def vignette(clone, dx, dy, radius, sigma):
    """add vignette into picture
    clone - clone of image for processing
    dx, dy - offset from border
    radius - radius of Gaussian blur
    sigma - standard deviation for Gaussian blur
    color - color of corners
    """
    # clone.vignette(
    #     radius=common.empty(radius),
    #     sigma=common.empty(sigma),
    #     x=common.empty(dx),
    #     y=common.empty(dy),
    # )
    # module_logger.debug(" Conversion: vigette")
    module_logger.warning("vigette not available for PILLOW, install ImageMagick")


def compose(clone, compose_file, right, autoresize, color, gravity):
    """join two pictures
    clone - clone of image for processing
    compose_file - file to join
    right - join on right or bottom side
    autoresize - autoresize picture or not
    color - color to fill gap if no autoresize
    gravity - position if no autoresize
    """
    result = None
    if os.path.exists(compose_file):
        clone_width, clone_height = clone.size
        with Image.open(compose_file) as compose_image:
            compose_image_width, compose_image_height = compose_image.size
            if right:
                if clone_height >= compose_image_height:
                    new_image_height = clone_height
                else:
                    new_image_height = compose_image_height
                if autoresize:
                    resize_width = int(
                        compose_image_width * clone_height / compose_image_height
                    )
                    resize_height = clone_height
                    new_image_width = clone_width + resize_width
                else:
                    new_image_width = clone_width + compose_image_width
                # for no autoresize
                position_x1 = 0
                position_x2 = clone_width
                if clone_height >= compose_image_height:
                    # orig > compose
                    position_y1 = 0
                    if gravity == "N":
                        position_y2 = 0
                    elif gravity == "S":
                        position_y2 = int(new_image_height - compose_image_height)
                    else:
                        position_y2 = int(
                            new_image_height / 2 - compose_image_height / 2
                        )
                    if autoresize:
                        position_y2 = 0
                else:
                    # orig < compose
                    position_y2 = 0
                    if gravity == "N":
                        position_y1 = 0
                    elif gravity == "S":
                        position_y1 = int(new_image_height - clone_height)
                    else:
                        position_y1 = int(new_image_height / 2 - clone_height / 2)
                    if autoresize:
                        position_y1 = 0
            else:
                # for canvas
                if clone_width >= compose_image_width:
                    new_image_width = clone_width
                else:
                    new_image_width = compose_image_width
                if autoresize:
                    resize_width = clone_width
                    resize_height = int(
                        compose_image_height * clone_width / compose_image_width
                    )
                    new_image_height = int(clone_height + resize_height)
                else:
                    new_image_height = int(clone_height + compose_image_height)
                # for no autoresize
                position_y1 = 0
                position_y2 = clone_height
                if clone_width >= compose_image_width:
                    # orig > compose
                    position_x1 = 0
                    if gravity == "W":
                        position_x2 = 0
                    elif gravity == "E":
                        position_x2 = int(new_image_width - compose_image_width)
                    else:
                        position_x2 = int(new_image_width / 2 - compose_image_width / 2)
                    if autoresize:
                        position_x2 = 0
                else:
                    # orig < compose
                    position_x2 = 0
                    if gravity == "W":
                        position_x1 = 0
                    elif gravity == "E":
                        position_x1 = int(new_image_width - clone_width)
                    else:
                        position_x1 = int(new_image_width / 2 - clone_width / 2)
                    if autoresize:
                        position_x1 = 0

            if autoresize:
                compose_image = compose_image.resize((resize_width, resize_height))

            image_new = Image.new("RGB", (new_image_width, new_image_height), color)
            image_new.paste(clone, (position_x1, position_y1))
            image_new.paste(compose_image, (position_x2, position_y2))
            result = image_new
    else:
        module_logger.warning(" Conversion: compose - missing file to compose")
    module_logger.debug(" Conversion: compose")
    return result


# ------------------------------------ Preview
def preview(file_in, max_size, operating_system, coord=""):
    """
    preview generation by Pillow
    file_in - fullname image file
    max_size - required size of image
    operating_system - operating system: Windows, MACOS, UNIX
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
                left_top = (coord[0], coord[1])
                right_bottom = (coord[2], coord[3])
                rectangle = (left_top, right_bottom)
                outline_color = "#FFFF00"
                if coord[0] < coord[2] and coord[1] < coord[3]:
                    draw = ImageDraw.Draw(clone)
                    draw.rectangle(rectangle, outline=outline_color, fill=None, width=2)
            preview_width, preview_height = clone.size
            file_preview = os.path.join(tempfile.gettempdir(), "fotokilof_preview.ppm")
            save_close_clone(clone, file_preview)
            result = {
                "filename": common.spacja(file_preview, operating_system),
                "size": filesize,
                "width": str(width),
                "height": str(height),
                "preview_width": str(preview_width),
                "preview_height": str(preview_height),
            }
            module_logger.debug("preview: %s", str(result))
    return result


# EOF
