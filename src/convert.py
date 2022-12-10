# -*- coding: utf-8 -*-

"""
Copyright (c) 2019-2022 Tomasz Łuczak, TeaM-TL

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
- convert_crop - crop picture
- convert_resize - resize picture
- convert_contrast - modify contrast
- convert_normalize - normalize levels
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


def convert_pip(gravitation, width, height, offset_dx, offset_dy):
    """ 9. Picture In Picture, eg. to add logo on image """

    command = "-gravity " + gravity(gravitation) \
        + " -geometry " + width + "x" + height \
        + "+" + offset_dx + "+" + offset_dy
    return command + " "


def gravity(gravitation):
    """ translate gravitation name according to Tk specification"""

    if gravitation == "N":
        result = "north"
    if gravitation == "NW":
        result = "north_west"
    if gravitation == "NE":
        result = "north_east"
    if gravitation == "W":
        result = "west"
    if gravitation == "C":
        result = "center"
    if gravitation == "E":
        result = "east"
    if gravitation == "SW":
        result = "south_west"
    if gravitation == "S":
        result = "south"
    if gravitation == "SE":
        result = "south_east"
    if gravitation == "0":
        result = "0"

    return result


# EOF
