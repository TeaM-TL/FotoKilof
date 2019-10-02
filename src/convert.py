# -*- coding: utf-8 -*-
# pylint: disable=line-too-long

""" moduł z konwerterami """

def convert_border(width, color):
    """ 1. dodanie ramki """

    # global img_border_color
    if int(width) > 0:
        command = "-border " + width + " -bordercolor \"" + color + "\""
    else:
        command = ""
    return command


def convert_text(entries):
    """ 2. Umieszczenie napisu na obrazku """

    if entries['text_convert'] == 1:
        size = " -pointsize " + entries['font_size']
        font = " -font '" + entries['font'] + "'"
        color = " -fill \"" + entries['text_color'] + "\""
        gravit = " -gravity " + gravity(entries['gravitation'])

        text = " -draw \"text " + entries['dx'] + "," + entries['dy'] + " '" + entries['text'] + "'\""
        if entries['box'] == 0:
            box = ""
        else:
            box = " -box \"" + entries['box_color'] + "\""
        command = box + color + size + gravit + font + text
    else:
        command = ""
    return command


def convert_crop(crop, gravitation, entries):
    """ 3. Wycięcie obrazka z obrazka """

    if crop > 0:
        if crop == 1:
            width = str(abs(int(entries['one_x2']) - int(entries['one_x1'])))
            height = str(abs(int(entries['one_y2']) - int(entries['one_y1'])))
            command = " -crop " + width + "x" + height + "+" + entries['one_x1'] + "+" + entries['one_y1']
        if crop == 2:
            command = " -crop " + entries['two_width'] + "x" + entries['two_height'] + "+" + entries['two_x1'] + "+" + entries['two_y1']
        if crop == 3:
            command = " -gravity " + gravity(gravitation) + " -crop " + entries['three_width'] + "x" + entries['three_height'] + "+" + entries['three_dx'] + "+" + entries['three_dy']
    else:
        command = ""
    return command


def convert_resize(resize, pixel, percent, border):
    """ 4. Zmiana rozmiaru obrazka """

    border = 2 * int(border)
    if resize == 0:
        command = ""
        return command
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
    """ 5. czarno-białe albo sepia """

    if black_white == 1:
        command = "-colorspace Gray"
    elif black_white == 2:
        command = "-sepia-tone " + str(int(sepia)) + "%"
    else:
        command = ""
    return command


def convert_contrast(contrast, contrast_selected, entry1, entry2):
    """ 6. Zmiana kontrastu """

    if contrast == 1:
        if contrast_selected == "+2":
            command = "+contrast +contrast"
        elif contrast_selected == "+1":
            command = "+contrast"
        elif contrast_selected == "-1":
            command = "-contrast"
        elif contrast_selected == "-2":
            command = "-contrast -contrast"
        else:
            command = ""
    elif contrast == 2:
        command = "-contrast-stretch " + entry1 + "x" + entry2 + "%"
    else:
        command = ""
    return command


def convert_normalize(normalize):
    """ 7. Normalizacja kolorów """

    if normalize == 1:
        command = "-normalize"
    elif normalize == 2:
        command = "-auto-level"
    else:
        command = ""
    return command


def convert_rotate(rotate):
    """ 8. Obrót obrazka o 90,180 albo 270stopni """

    if rotate > 0:
        command = "-rotate " + str(rotate)
    else:
        command = ""
    return command


def gravity(gravitation):
    """ nazwy grawitacji zgodne z Tk """

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
