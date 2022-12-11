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
- preview_crop_gravity - convert corrdinates from crop3
- gravity - translate eg. NS to Northsouth as Wand-py expect
"""

def preview_crop_gravity(coordinates, x_max, y_max):
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


def gravitation(gravitation):
    """ translate gravitation name from Tk to Wand-py specification"""

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
