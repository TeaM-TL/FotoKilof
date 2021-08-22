# -*- coding: utf-8 -*-

"""
Copyright (c) 2019-2021 Tomasz Łuczak, TeaM-TL

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
- convert_preview_crop_gravity - convert corrdinates from crop3
- convert_border - add border to picture
- convert_text - add text
- convert_crop - crop picture
- convert_resize - resize picture
- convert_contrast - modify contrast
- convert_normalize - normalize levels
- convert_rotate - rotate picture
- convert_mirror - mirroring picture
- convert_pip - picture in picture, for inserting logo
- gravity - translate eg. NS to Northsouth as Tk expect
- gravity_outside - translate gravitation for adding text outside
"""

def convert_preview_crop_gravity(coordinates, x_max, y_max):
    """
    convert corrdinates from crop3:
    offset_x, offset_y, width, height, gravitation
    original image size:
    x_max, y_max
    return coordinates for drawing crop: x0, y0, x1, y1
    """
    offset_x = coordinates[0]
    offset_y = coordinates[1]
    width = coordinates[2]
    height = coordinates[3]
    gravitation = coordinates[4]
    if gravitation == "NW":
        x0 = offset_x
        y0 = offset_y
        x1 = x0 + width
        y1 = y0 + height
    elif gravitation == "N":
        x0 = x_max/2 - width/2
        y0 = offset_y
        x1 = x_max/2 + width/2
        y1 = y0 + height
    elif gravitation == "NE":
        x0 = x_max - width - offset_x
        y0 = offset_y
        x1 = x_max - offset_x
        y1 = y0 + height
    elif gravitation == "W":
        x0 = offset_x
        y0 = y_max/2 - height/2
        x1 = x0 + width
        y1 = y_max/2 + height/2
    elif gravitation == "C":
        x0 = x_max/2 - width/2
        y0 = y_max/2 - height/2
        x1 = x_max/2 + width/2
        y1 = y_max/2 + height/2
    elif gravitation == "E":
        x0 = x_max - width - offset_x
        y0 = y_max/2 - height/2
        x1 = x_max - offset_x
        y1 = y_max/2 + height/2
    elif gravitation == "SW":
        x0 = offset_x
        y0 = y_max - height - offset_y
        x1 = x0 + width
        y1 = y_max - offset_y
    elif gravitation == "S":
        x0 = x_max/2 - width/2
        y0 = y_max - height - offset_y
        x1 = x_max/2 + width/2
        y1 = y_max - offset_y
    elif gravitation == "SE":
        x0 = x_max - width - offset_x
        y0 = y_max - height - offset_y
        x1 = x_max - offset_x
        y1 = y_max - offset_y
    else:
        x0 = 5
        y0 = 5
        x1 = x_max - 5
        y1 = y_max -5
    return (x0, y0, x1, y1)


def convert_border(width, color, border_on):
    """ 1. Add border """

    if border_on > 0:
        command = " -bordercolor \"" + color + "\"" + \
                  " -border " + str(abs(int(width))) + " "
    else:
        command = ""
    return command + " "


def convert_text(entries):
    """ 2. Insert text into picture """

    if entries['text_on'] == 1:
        size = ' -pointsize ' + entries['font_size']
        font = ' -font "' + entries['font'] + '"'
        color = ' -fill "' + entries['text_color'] + '"'

        if entries['text_inout'] == 0:
            # inside
            outside = ""
            if entries['gravitation_onoff'] == 0:
                gravitation = " "
            else:
                gravitation = " -gravity " + gravity(entries['gravitation'])
            text = " -draw \"text " + entries['dx'] + "," + entries['dy'] \
                + " '" + entries['text'] + "'\" "
            if entries['box'] == 0:
                box = ""
            else:
                box = " -box \"" + entries['box_color'] + "\""
        else:
            # outside
            gravitation = " -gravity " + gravity(entries['gravitation'])
            text = " label:\"" + entries['text'] + "\" "
            # position
            if entries['gravitation'] == "NW" or entries['gravitation'] == "N" or entries['gravitation'] == "NE":
                # top
                outside = "+swap -append "
            else:
                # bottom
                outside = "-append "
            # background
            if entries['box'] == 0:
                box = ""
            else:
                box = " -background \"" + entries['box_color'] + "\""

        command = box + color + size + gravitation + font + text + outside
    else:
        command = ""
    return command + " "


def convert_crop(crop, gravitation, entries):
    """ 3. Crop """

    if crop == 1:
        width = str(abs(int(entries['one_x2']) - int(entries['one_x1'])))
        height = str(abs(int(entries['one_y2']) - int(entries['one_y1'])))
        command = " -crop " + width + "x" + height \
            + "+" + entries['one_x1'] + "+" + entries['one_y1']
    if crop == 2:
        command = " -crop " \
            + entries['two_width'] + "x" + entries['two_height'] \
            + "+" + entries['two_x1'] + "+" + entries['two_y1']
    if crop == 3:
        command = " -gravity " + gravity(gravitation) + " -crop " \
            + entries['three_width'] + "x" + entries['three_height'] \
            + "+" + entries['three_dx'] + "+" + entries['three_dy']
    return command + " "


def convert_resize(resize, pixel, percent, border):
    """ 4. Resize """

    # słownik wyjściowy
    dict_return = {}
    border = 2 * abs(int(border))

    if resize == 0:
        command = ""
        sub_dir = ""
    if resize == 1:
        command = "-resize " + pixel + "x" + pixel + " "
        sub_dir = pixel
    elif resize == 2:
        command = "-resize " + percent + "% "
        sub_dir = percent
    elif resize == 3:
        command = "-resize " + str(1920 - border) + "x" + str(1080 - border) + " "
        sub_dir = "1920x1080"
    elif resize == 4:
        command = "-resize " + str(2048 - border) + "x" + str(1556 - border) + " "
        sub_dir = "2048x1556"
    elif resize == 5:
        command = "-resize " + str(4096 - border) + "x" + str(3112 - border) + " "
        sub_dir = "4096x3112"

    dict_return['command'] = command
    dict_return['sub_dir'] = sub_dir
    return dict_return


def convert_bw(black_white, sepia):
    """ 5. black-white or  sepia """

    if black_white == 1:
        command = "-colorspace Gray"
    elif black_white == 2:
        command = "-sepia-tone " + str(int(sepia)) + "%"
    else:
        command = ""
    return command + " "


def convert_contrast(contrast, contrast_selected, entry1, entry2):
    """ 6. Contrast """

    command = ""
    if contrast == 1:
        command = "-contrast-stretch " + entry1 + "x" + entry2 + "%"
    elif contrast == 2:
        if contrast_selected == "+3":
            command = "+contrast +contrast +contrast"
        elif contrast_selected == "+2":
            command = "+contrast +contrast"
        elif contrast_selected == "+1":
            command = "+contrast"
        elif contrast_selected == "0":
            command = ""
        elif contrast_selected == "-1":
            command = "-contrast"
        elif contrast_selected == "-2":
            command = "-contrast -contrast"
        elif contrast_selected == "-3":
            command = "-contrast -contrast -contrast"
        else:
            command = ""
    elif contrast == 3:
        command = "-normalize"
    else:
        command = ""
    return command + " "


def convert_normalize(normalize, channel):
    """ 7. Normalize """

    if normalize == 1:
        if channel != "None":
            command = "-channel " + channel + " -equalize"
        else:
            command = "-equalize"
    elif normalize == 2:
        command = "-auto-level"
    else:
        command = ""
    return command + " "


def convert_rotate(rotate):
    """ 8. Rotate 90,180, 270 degree """

    if rotate > 0:
        command = "-rotate " + str(rotate)
    else:
        command = ""
    return command + " "


def convert_mirror(flip, flop):
    """ 10. Mirror: flip or flop """

    if flip:
        command_flip = "-flip "
    else:
        command_flip = ""
    if flop:
        command_flop = "-flop "
    else:
        command_flop = ""
    return command_flip + command_flop + " "


def convert_pip(gravitation, width, height, offset_dx, offset_dy):
    """ 9. Picture In Picture, eg. to add logo on image """

    command = "-gravity " + gravity(gravitation) \
        + " -geometry " + width + "x" + height \
        + "+" + offset_dx + "+" + offset_dy
    return command + " "


def gravity(gravitation):
    """ translate gravitation name according to Tk specification"""

    if gravitation == "N":
        result = "North"
    if gravitation == "NW":
        result = "Northwest"
    if gravitation == "NE":
        result = "Northeast"
    if gravitation == "W":
        result = "West"
    if gravitation == "C":
        result = "Center"
    if gravitation == "E":
        result = "East"
    if gravitation == "SW":
        result = "Southwest"
    if gravitation == "S":
        result = "South"
    if gravitation == "SE":
        result = "Southeast"
    if gravitation == "0":
        result = "0"

    return result


# EOF
