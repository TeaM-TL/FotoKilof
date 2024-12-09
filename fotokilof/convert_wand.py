# -*- coding: utf-8 -*-
# pylint: disable=bare-except

"""
Copyright (c) 2022-2024 Tomasz Łuczak, TeaM-TL

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
- preview - preview done by Wand
"""

import logging
import tempfile
import os
import os.path

try:
    from wand.drawing import Drawing
    from wand.image import Image
    from wand.version import fonts as fontsList

    WAND_TEXT = "Wand and ImageMagics found"
except:
    WAND_TEXT = "ImageMagick or Wand-py not found"

# my modules
import common


module_logger = logging.getLogger(__name__)
module_logger.info(WAND_TEXT)


# ------------------------------------ Info
def fonts_list():
    """list of available fonts"""
    return fontsList()


# ------------------------------------ Common
def make_clone(file_to_clone, color=None):
    """open picture and make clone for processing"""
    if file_to_clone:
        with Image(filename=file_to_clone, background=color) as image:
            return image.clone()
    else:
        return None


def save_close_clone(clone, file_out, exif=0):
    """save and close clone after processing"""
    if clone is None:
        module_logger.error(" Clone for %s is None", file_out)
    else:
        if not exif:
            clone.strip()
        with open(file_out, "wb") as file_handler:
            clone.save(file=file_handler)
            module_logger.debug(" Save file: %s", file_out)
        clone.close()


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


def rotate(clone, angle, color, angle_own):
    """rotate"""
    if angle == 0:
        angle = common.empty(angle_own)
        if angle == 0:
            color = None
    clone.rotate(angle, background=color)


def mirror(clone, flip, flop):
    """mirror: flip and flop"""
    if flip:
        clone.flip()
    if flop:
        clone.flop()


def border(clone, color, x, y):
    """border: color, x, y"""
    clone.border(color, common.empty(x), common.empty(y))


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
    arrow = convert_data[14]

    image_width, image_height = clone.size

    if text_string:
        gravity_common, new_x, new_y = common.gravitation(
            gravity, int(text_x), int(text_y), image_width, image_height
        )
        draw_gravity = gravity_common[1]
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
        if arrow:
            if gravity_onoff == 0:
                gravity = "NW"

            arrow_coord_all = common.gravitation(
                gravity,
                int(text_x),
                int(text_y),
                image_width,
                image_height,
            )
            arrow_coord = (arrow_coord_all[1], arrow_coord_all[2])
            a, c, d, e, offset_x, offset_y = common.arrow_gravity(
                gravity, text_size, arrow_coord[0], arrow_coord[1]
            )
        else:
            offset_x = 0
            offset_y = 0
        text_x = int(int(text_x) + abs(offset_x))
        text_y = int(int(text_y) + abs(offset_y))
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
            if arrow:
                if gravity_onoff == 0:
                    gravity = "NW"
                with Drawing() as draw_arrow:
                    draw_arrow.fill_color = text_color
                    draw_arrow.line(a, c)
                    draw_arrow.line(d, c)
                    draw_arrow.line(e, c)
                    draw_arrow(clone)
        else:
            # outside
            metrics = draw.get_font_metrics(clone, text_string, multiline=False)
            with Image(
                width=image_width,
                height=int(metrics.text_height),
                background=backgroud_color,
            ) as canvas:
                canvas.annotate(text_string, draw)
                clone.sequence.append(canvas)
                clone.concat(stacked=True)
    return clone


def bw(clone, bw_variant, sepia):
    """black and white or sepia"""
    if bw_variant == 1:
        # black-white
        clone.type = "grayscale"
    else:
        # sepia
        clone.sepia_tone(threshold=common.empty(sepia) / 100)


def resize(clone, command):
    """resize picture"""
    clone.transform(crop="", resize=command)


def normalize(clone, normalize_variant, channel):
    """normalize levels of colors"""
    if normalize_variant == 1:
        if channel != "None":
            clone.alpha_channel = True
            clone.normalize(channel=channel)
        else:
            clone.normalize()
    else:
        clone.auto_level()


def contrast(clone, contrast_variant, selection, black, white):
    """normalize levels of colors"""
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


def crop(clone, crop_variant, coordinates):
    """
    crop picture
    entries are as dictionary
    """

    match crop_variant:
        case 1:
            clone.crop(
                left=coordinates[0],
                top=coordinates[1],
                right=coordinates[2],
                bottom=coordinates[3],
            )
        case 2:
            clone.crop(
                left=coordinates[0],
                top=coordinates[1],
                width=coordinates[2],
                height=coordinates[3],
            )
        case 3:
            clone.crop(
                left=coordinates[0],
                top=coordinates[1],
                width=coordinates[2],
                height=coordinates[3],
                gravity=coordinates[4],
            )


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


def compose(clone, compose_file, right, autoresize, color, gravity):
    """join two pictures
    clone - clone of image for processing
    compose_file - file to join
    right - join on right or bottom side
    autoresize - autoresize picture or not
    color - color to fill gap if no autoresize
    gravity - position if no autoresize
    """
    if os.path.exists(compose_file):
        with Image(filename=compose_file) as compose_image:
            compose_width = compose_image.width
            compose_height = compose_image.height
            position_1, position_2, new_size, resize_factor = (
                common.compose_calculation(
                    clone.size,
                    (compose_width, compose_height),
                    autoresize,
                    right,
                    gravity,
                )
            )
            if autoresize:
                if right:
                    stacked = False
                else:
                    stacked = True
                resize_value = (
                    str(int(compose_width * resize_factor))
                    + "x"
                    + str(int(compose_height * resize_factor))
                )
                compose_image.transform(crop="", resize=resize_value)
                clone.sequence.append(compose_image)
                clone.concat(stacked=stacked)
            else:
                if right:
                    left = position_1[0]
                    top = position_1[1]
                else:
                    left = position_1[1]
                    top = position_1[0]
                with Image(
                    width=new_size[0], height=new_size[1], background=color
                ) as image_new:
                    image_new.format = os.path.splitext(compose_file)[1].split(".")[1]
                    image_new.composite(clone, left=left, top=top)
                    image_new.composite(
                        compose_image, left=position_2[0], top=position_2[1]
                    )
                    clone.image_set(image_new)
    else:
        module_logger.warning(" Conversion: compose - missing file to compose")

    return clone


# ------------------------------------ Preview
def preview(file_in, size, operating_system, coord=""):
    """
    preview generation by Wand
    file_in - fullname image file
    size - required size of image
    os - operating system: Windows, MACOS, UNIX
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

    if file_in:
        if os.path.isfile(file_in):
            filesize = common.humansize(os.path.getsize(file_in))
            clone = make_clone(file_in)
            width, height = clone.size
            resize(clone, str(size) + "x" + str(size))
            # write crop if coordinates are given
            if len(coord) == 4:
                with Drawing() as draw:
                    left_top = (coord[0], coord[1])
                    left_bottom = (coord[0], coord[3])
                    right_top = (coord[2], coord[1])
                    right_bottom = (coord[2], coord[3])
                    draw.fill_color = "#FFFF00"
                    # draw.rectangle(left=coord[0], top=coord[1], right=coord[2], bottom=coord[3])
                    draw.line(left_top, right_top)
                    draw.line(left_top, left_bottom)
                    draw.line(left_bottom, right_bottom)
                    draw.line(right_top, right_bottom)
                    draw(clone)
            preview_width, preview_height = clone.size
            file_preview = os.path.join(tempfile.gettempdir(), "fotokilof_preview.ppm")
            with clone.convert("ppm") as converted:
                save_close_clone(converted, file_preview)
            result = {
                "filename": common.spacja(file_preview, operating_system),
                "size": filesize,
                "width": str(width),
                "height": str(height),
                "preview_width": str(preview_width),
                "preview_height": str(preview_height),
            }

    return result


# EOF
