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
- get_image_size - get size from image
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
    if len(file_to_clone):
        with Image(filename=file_to_clone, background=color) as image:
            result = image.clone()
    else:
        result = None
    return result


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
                with Image(filename=filename) as image:
                    size = image.size
            except:
                module_logger.error(" Error read file: %s", filename)
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


def rotate(clone, angle, color, angle_own):
    """rotate"""
    if angle == 0:
        angle = common.empty(angle_own)
    if angle == 0:
        color = None
    clone.rotate(angle, background=color)
    module_logger.debug(" Conversion: rotate %s", str(angle))


def mirror(clone, flip, flop):
    """mirror: flip and flop"""
    if flip:
        clone.flip()
    if flop:
        clone.flop()
    module_logger.debug(" Conversion: mirror")


def border(clone, color, x, y):
    """border: color, x, y"""
    clone.border(color, common.empty(x), common.empty(y))
    module_logger.debug(" Conversion: border")


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
    arrow = 0

    if len(text_string):
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
        if arrow:
            if gravity_onoff == 0:
                gravity = "NW"
            a, c, d, e, offset_x, offset_y = common.arrow_gravity(gravity, text_size, text_x, text_y)
        else:
            offset_x = 0
            offset_y = 0
        text_x = str(int(text_x) + offset_x)
        text_y = str(int(text_y) + offset_y)
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
                # a, c, d, e, offset_x, offset_y = common.arrow_gravity(gravity, text_size, text_x, text_y)
                if gravity != "C":
                    print(a, c, d, e)
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
                width=clone.width,
                height=int(metrics.text_height),
                background=backgroud_color,
            ) as canvas:
                canvas.annotate(text_string, draw)
                clone.sequence.append(canvas)
                clone.concat(stacked=True)
    module_logger.debug(" Conversion: text %s", str(in_out))
    return clone


def bw(clone, bw_variant, sepia):
    """black and white or sepia"""
    if bw_variant == 1:
        # black-white
        clone.type = "grayscale"
    else:
        # sepia
        clone.sepia_tone(threshold=common.empty(sepia) / 100)
    module_logger.debug(" Conversion: black-white/sepia %s", str(bw_variant))


def resize(clone, command):
    """resize picture"""
    clone.transform(crop="", resize=command)
    module_logger.debug(" Conversion: resize")


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
    module_logger.debug(" Conversion: normalize %s", str(normalize_variant))


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
    module_logger.debug(" Conversion: contrast %s", str(contrast_variant))


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
    module_logger.debug(" Conversion: crop %s", str(crop_variant))


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
    module_logger.debug(" Conversion: vigette")


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
        clone_width, clone_height = clone.size
        with Image(filename=compose_file) as compose_image:
            compose_image_width, compose_image_height = compose_image.size
            if right:
                stacked = False
                # for canvas
                canvas_width = clone_width + compose_image_width
                if clone_height >= compose_image_height:
                    canvas_height = clone_height
                else:
                    canvas_height = compose_image_height
                # for autoresize
                resize_width = int(
                    compose_image_width * clone_height / compose_image_height
                )
                resize_height = clone_height
                # for no autoresize
                position_x1 = 0
                position_x2 = clone_width
                if clone_height >= compose_image_height:
                    # orig > compose
                    position_y1 = 0
                    if gravity == "N":
                        position_y2 = 0
                    elif gravity == "S":
                        position_y2 = int(canvas_height - compose_image_height)
                    else:
                        position_y2 = int(canvas_height / 2 - compose_image_height / 2)
                else:
                    # orig < compose
                    position_y2 = 0
                    if gravity == "N":
                        position_y1 = 0
                    elif gravity == "S":
                        position_y1 = int(canvas_height - clone_height)
                    else:
                        position_y1 = int(canvas_height / 2 - clone_height / 2)
            else:
                stacked = True
                # for canvas
                if clone_width >= compose_image_width:
                    canvas_width = clone_width
                else:
                    canvas_width = compose_image_width
                canvas_height = int(clone_height + compose_image_height)
                # for autoresize
                resize_width = clone_width
                resize_height = int(
                    compose_image_height * clone_width / compose_image_width
                )
                # for no autoresize
                position_y1 = 0
                position_y2 = clone_height
                if clone_width >= compose_image_width:
                    # orig > compose
                    position_x1 = 0
                    if gravity == "W":
                        position_x2 = 0
                    elif gravity == "E":
                        position_x2 = int(canvas_width - compose_image_width)
                    else:
                        position_x2 = int(canvas_width / 2 - compose_image_width / 2)
                else:
                    # orig < compose
                    position_x2 = 0
                    if gravity == "W":
                        position_x1 = 0
                    elif gravity == "E":
                        position_x1 = int(canvas_width - clone_width)
                    else:
                        position_x1 = int(canvas_width / 2 - clone_width / 2)

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
                            width=clone_width,
                            height=clone_height,
                            image=clone,
                        )
                        draw(canvas)
                        # picture to join
                        draw.composite(
                            operator="over",
                            left=position_x2,
                            top=position_y2,
                            width=compose_image_width,
                            height=compose_image_height,
                            image=compose_image,
                        )
                        draw(canvas)
                    clone.image_set(canvas)
    else:
        module_logger.warning(" Conversion: compose - missing file to compose")

    module_logger.debug(" Conversion: compose")
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

    if file_in is not None:
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
