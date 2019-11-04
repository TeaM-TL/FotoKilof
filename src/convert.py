# -*- coding: utf-8 -*-
""" Converters """


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
        command = "-border " + str(abs(int(width))) + \
            " -bordercolor \"" + color + "\""
    else:
        command = ""
    return command


def convert_text(entries):
    """ 2. Umieszczenie napisu na obrazku """

    if entries['text_on'] == 1:
        size = " -pointsize " + entries['font_size']
        font = " -font '" + entries['font'] + "'"
        color = " -fill \"" + entries['text_color'] + "\""
        gravit = " -gravity " + gravity(entries['gravitation'])

        text = " -draw \"text " + entries['dx'] + "," + entries['dy'] \
            + " '" + entries['text'] + "'\""
        if entries['box'] == 0:
            box = ""
        else:
            box = " -box \"" + entries['box_color'] + "\""
        command = box + color + size + gravit + font + text
    else:
        command = ""
    return command


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
    return command


def convert_resize(resize, pixel, percent, border):
    """ 4. Resize """

    border = 2 * abs(int(border))
    if resize == 1:
        image_resize = pixel + "x" + pixel
    elif resize == 2:
        image_resize = percent + "%"
    elif resize == 3:
        image_resize = str(1920 - border) + "x" + str(1080 - border)
    elif resize == 4:
        image_resize = str(2048 - border) + "x" + str(1556 - border)
    elif resize == 5:
        image_resize = str(4096 - border) + "x" + str(3112 - border)

    command = "-resize " + image_resize
    return command


def convert_bw(black_white, sepia):
    """ 5. black-white or  sepia """

    if black_white == 1:
        command = "-colorspace Gray"
    elif black_white == 2:
        command = "-sepia-tone " + str(int(sepia)) + "%"
    else:
        command = ""
    return command


def convert_contrast(contrast, contrast_selected, entry1, entry2):
    """ 6. Contrast """

    if contrast == 1:
        if contrast_selected == "+3":
            command = "+contrast +contrast +contrast"
        elif contrast_selected == "+2":
            command = "+contrast +contrast"
        elif contrast_selected == "+1":
            command = "+contrast"
        elif contrast_selected == "-1":
            command = "-contrast"
        elif contrast_selected == "-2":
            command = "-contrast -contrast"
        elif contrast_selected == "-3":
            command = "-contrast -contrast -contrast"
        else:
            command = ""
    elif contrast == 2:
        command = "-contrast-stretch " + entry1 + "x" + entry2 + "%"
    else:
        command = ""
    return command


def convert_normalize(normalize, channel):
    """ 7. Normalize """

    if normalize == 1:
        command = "-normalize"
    elif normalize == 2:
        command = "-auto-level"
    elif normalize == 3:
        if channel != "None":
            command = "-channel " + channel + " -equalize"
        else:
            command = "-equalize"
    else:
        command = ""
    return command


def convert_rotate(rotate):
    """ 8. Rotate 90,180, 270 degree """

    if rotate > 0:
        command = "-rotate " + str(rotate)
    else:
        command = ""
    return command


def convert_pip(gravitation, width, height, offset_dx, offset_dy):
    """ 9. Picture In Picture, eg. to add logo on image """

    command = "-gravity " + gravity(gravitation) \
        + " -geometry " + width + "x" + height \
        + "+" + offset_dx + "+" + offset_dy
    return command


def gravity(gravitation):
    """ translate gavitation name according to Tk specification"""

    if gravitation == "N":
        gravitation = "North"
    if gravitation == "NW":
        gravitation = "Northwest"
    if gravitation == "NE":
        gravitation = "Northeast"
    if gravitation == "W":
        gravitation = "West"
    if gravitation == "C":
        gravitation = "Center"
    if gravitation == "E":
        gravitation = "East"
    if gravitation == "SW":
        gravitation = "Southwest"
    if gravitation == "S":
        gravitation = "South"
    if gravitation == "SE":
        gravitation = "Southeast"

    return gravitation

# EOF
