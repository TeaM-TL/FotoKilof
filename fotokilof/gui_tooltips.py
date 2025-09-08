# -*- coding: utf-8 -*-
# pylint: disable=bare-except
# pylint: disable=too-many-branches
# pylint: disable=too-many-lines
# pylint: disable=too-many-statements
# pylint: disable=invalid-name
# pylint: disable=line-too-long

"""
Copyright (c) 2025 Tomasz Łuczak, TeaM-TL

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

nice GUI for ImageMagick command common used (by me)
"""

from ttkbootstrap.tooltip import ToolTip


def init_tooltips(widgets):
    """tooltips inicjalization"""

    def tooltip_if_exists(widget, text):
        if widget is not None:
            ToolTip(widget, text=text)

    tooltip_if_exists(
        widgets.get("b_file_select"), text=_("Select image file for processing")
    )
    tooltip_if_exists(
        widgets.get("b_file_select_screenshot"),
        text=_(
            "Get image from clipboard.\nGrabbed image is saved into %TEMP%/today or $TMP/today directory and load for processing.\nLinux or BSD - install xclip"
        ),
    )
    tooltip_if_exists(
        widgets.get("b_file_select_first"),
        text=_("Load first image from current directory.\nUse Home key instead"),
    )
    tooltip_if_exists(
        widgets.get("b_file_select_prev"),
        text=_("Load previous image from current directory.\nUse PgUp key instead"),
    )
    tooltip_if_exists(
        widgets.get("b_file_select_next"),
        text=_("Load next image from current directory.\nUse PgDn key instead"),
    )
    tooltip_if_exists(
        widgets.get("b_file_select_last"),
        text=_("Load last image from current directory.\nUse End key instead"),
    )
    tooltip_if_exists(
        widgets.get("rb_apply_dir"), text=_("Processing all files in current directory")
    )
    tooltip_if_exists(
        widgets.get("rb_apply_file"), text=_("Processing only current file")
    )
    tooltip_if_exists(
        widgets.get("co_apply_type"),
        text=_("Selection of format output file; JPG, PNG or TIF"),
    )
    tooltip_if_exists(
        widgets.get("b_apply_run"),
        text=_(
            "Perform all selected conversion for current file or all files in current directory"
        ),
    )
    tooltip_if_exists(
        widgets.get("b_last_save"),
        text=_(
            "Save all values into configuration file (~/.fotokilof.ini).\nFotoKilof will load it during starting"
        ),
    )
    tooltip_if_exists(
        widgets.get("b_last_read"), text=_("Load saved values of conversion")
    )
    # main second
    tooltip_if_exists(
        widgets.get("cb_resize"),
        text=_(
            "Scale image, proportions are saved.\nSpecify maximum dimensions of image or percent"
        ),
    )
    tooltip_if_exists(
        widgets.get("cb_crop"),
        text=_(
            "Take part of image. Select crop by:\n- absolute coordinate\n- absolute coorinate left-top corner plus width and height\n- gravity plus width and height plus offset.\nRemember point (0,0) is located in left-top corner of image."
        ),
    )
    tooltip_if_exists(
        widgets.get("cb_text"),
        text=_(
            "Insert text on picture or add text at bottom.\nText can be rotated, colored and with background.\nAll font from OS are available"
        ),
    )
    tooltip_if_exists(
        widgets.get("cb_rotate"),
        text=_(
            "Rotate picture by 90, 180, 270 degree or specify own angle of rotation"
        ),
    )
    tooltip_if_exists(
        widgets.get("cb_border"),
        text=_(
            "Add border around picture.\nSpecify width of horizontal and vertical border separately"
        ),
    )
    tooltip_if_exists(widgets.get("cb_bw"), text=_("Convert into black-white or sepia"))
    tooltip_if_exists(
        widgets.get("cb_contrast"),
        text=_("Change contrast or change range of contrast"),
    )
    tooltip_if_exists(widgets.get("cb_normalize"), text=_("Normalize of color level"))
    tooltip_if_exists(
        widgets.get("cb_mirror"),
        text=_("Make mirror of picture in vertical or horizotal or both direction"),
    )
    tooltip_if_exists(
        widgets.get("cb_vignette"),
        text=_("Add vignette as on old photography or not the best lens"),
    )
    tooltip_if_exists(
        widgets.get("cb_logo"), text=_("Insert picture, eg. own logo, into picture")
    )
    tooltip_if_exists(
        widgets.get("cb_custom"),
        text=_("Processing ImageMagick command.\nWorks only on Linux OS"),
    )
    tooltip_if_exists(
        widgets.get("cb_exif"),
        text=_("If ON keep EXIF data\nif OFF EXIF data will be removed"),
    )
    # preview
    tooltip_if_exists(
        widgets.get("b_preview_orig_run"),
        text=_("Display original image by IMdisplay or default image viewer of OS"),
    )
    tooltip_if_exists(
        widgets.get("co_preview_selector_orig"), text=_("Select size of preview")
    )
    tooltip_if_exists(
        widgets.get("b_preview_new_run"),
        text=_("Display result image by IMdisplay or default image viewer of OS"),
    )
    tooltip_if_exists(
        widgets.get("co_preview_selector_new"), text=_("Select size of preview")
    )
    # Scaling
    tooltip_if_exists(
        widgets.get("b_resize_run"),
        text=_("Execute only resize conversion on current picture"),
    )
    # Crop
    tooltip_if_exists(
        widgets.get("rb1_crop"),
        text=_(
            "Select crop by absolute coordinate.\nRemember point (0,0) is located in left-top corner of image."
        ),
    )
    tooltip_if_exists(
        widgets.get("rb2_crop"),
        text=_(
            "Select crop by absolute coorinate left-top corner plus width and height.\nRemember point (0,0) is located in left-top corner of image."
        ),
    )
    tooltip_if_exists(
        widgets.get("rb3_crop"),
        text=_(
            "Select crop by gravity plus width and height plus offset.\nRemember point (0,0) is located in left-top corner of image."
        ),
    )
    tooltip_if_exists(
        widgets.get("e1_crop_1"),
        text=_(
            "x1 - horizontal position of left-top corner of crop\nClick left mouse button on preview in place of left-top corner"
        ),
    )
    tooltip_if_exists(
        widgets.get("e2_crop_1"),
        text=_(
            "y1 - vertical position of left-top corner of crop\nClick left mouse button on preview in place of left-top corner"
        ),
    )
    tooltip_if_exists(
        widgets.get("e3_crop_1"),
        text=_(
            "x2 - horizontal position of right-bottom corner of crop\nClick right mouse button on preview in place of left-top corner"
        ),
    )
    tooltip_if_exists(
        widgets.get("e4_crop_1"),
        text=_(
            "y2 - vertical position of right-bottom corner of crop\nClick right mouse button on preview in place of left-top corner"
        ),
    )
    tooltip_if_exists(
        widgets.get("e1_crop_2"),
        text=_("x1 - horizontal position of left-top corner of crop"),
    )
    tooltip_if_exists(
        widgets.get("e2_crop_2"),
        text=_("y1 - vertical position of left-top corner of crop"),
    )
    tooltip_if_exists(widgets.get("e3_crop_2"), text=_("X - width of crop"))
    tooltip_if_exists(widgets.get("e4_crop_2"), text=_("Y - height of crop"))
    tooltip_if_exists(
        widgets.get("e1_crop_3"), text=_("dx - horizontal offset from gravity point")
    )
    tooltip_if_exists(
        widgets.get("e2_crop_3"), text=_("dy - vertical offsef from gravity point")
    )
    tooltip_if_exists(widgets.get("e3_crop_3"), text=_("X - width of crop"))
    tooltip_if_exists(widgets.get("e4_crop_3"), text=_("Y - height of crop"))
    tooltip_if_exists(
        widgets.get("b_crop_read"),
        text=_(
            "Take size of crop from current picture.\nCrop will be 100% of original picture"
        ),
    )
    tooltip_if_exists(
        widgets.get("b_crop_show"), text=_("Refresh preview to see crop on picture")
    )
    tooltip_if_exists(
        widgets.get("frame_crop_gravity"),
        text=_("Use gravity direction for select crop"),
    )
    tooltip_if_exists(
        widgets.get("b_crop_run"),
        text=_("Execute only crop conversion on current picture"),
    )
    # Text
    tooltip_if_exists(widgets.get("e_text"), text=_("Click here and type text"))
    tooltip_if_exists(widgets.get("e_text_size"), text=_("Text size"))
    tooltip_if_exists(widgets.get("e_text_angle"), text=_("Angle of text"))
    tooltip_if_exists(widgets.get("co_text_font"), text=_("Font"))
    tooltip_if_exists(widgets.get("rb_text_in"), text=_("Put text on picture"))
    tooltip_if_exists(widgets.get("rb_text_out"), text=_("Put text below picture"))
    tooltip_if_exists(
        widgets.get("cb_text_gravity"),
        text=_("Use gravity for putting text or Absolute position"),
    )
    tooltip_if_exists(
        widgets.get("frame_text_gravity"),
        text=_("Use gravity direction for text placement"),
    )
    tooltip_if_exists(widgets.get("cb_text_box"), text=_("Use background for text"))
    tooltip_if_exists(
        widgets.get("cb_text_arrow"), text=_("Add arrow between text and origin point")
    )
    tooltip_if_exists(
        widgets.get("e_text_x"), text=_("Offset from gravity or absolute position")
    )
    tooltip_if_exists(
        widgets.get("e_text_y"), text=_("Offset from gravity or absolute position")
    )
    tooltip_if_exists(
        widgets.get("l_text_color"), text=_("Selected color of text and background")
    )
    tooltip_if_exists(widgets.get("b_text_color"), text=_("Select color of text"))
    tooltip_if_exists(
        widgets.get("b_text_box_color"), text=_("Select color of background")
    )
    tooltip_if_exists(
        widgets.get("b_text_run"), text=_("Execute only adding text on current picture")
    )
    # Rotate
    tooltip_if_exists(
        widgets.get("rb_rotate_own"),
        text=_("Select if want to use own angle of rotation"),
    )
    tooltip_if_exists(
        widgets.get("e_rotate_own"),
        text=_(
            "Put angle of rotation. Rotation is in right direction.\nBackground color is as choosed by Color button"
        ),
    )
    tooltip_if_exists(
        widgets.get("l_rotate_color"), text=_("Selected color to fill a gap")
    )
    tooltip_if_exists(
        widgets.get("b_rotate_color"),
        text=_("If OWN is choosed, select color to fill a gap."),
    )
    tooltip_if_exists(
        widgets.get("b_rotate_run"),
        text=_("Execute only rotate conversion on current picture"),
    )
    # Scaling
    tooltip_if_exists(
        widgets.get("e2_resize"), text=_("Put percent for rescale of picture")
    )
    tooltip_if_exists(
        widgets.get("b_resize_run"),
        text=_("Execute only resize conversion on current picture"),
    )
    # Border
    tooltip_if_exists(
        widgets.get("e_border_ns"), text=_("Put width of vertical part of border")
    )
    tooltip_if_exists(
        widgets.get("e_border_we"), text=_("Put width of horizontal part of border")
    )
    tooltip_if_exists(widgets.get("l_border_color"), text=_("Selected color of border"))
    tooltip_if_exists(widgets.get("b_border_color"), text=_("Select color of border"))
    tooltip_if_exists(
        widgets.get("b_border_run"),
        text=_("Execute only add border conversion on current picture"),
    )
    # Black-white
    tooltip_if_exists(
        widgets.get("rb1_bw"), text=_("Convert picture into gray scale - black-white")
    )
    tooltip_if_exists(
        widgets.get("rb2_bw"),
        text=_("Convert picture into sepia - old style silver based photography"),
    )
    tooltip_if_exists(
        widgets.get("e_bw_sepia"),
        text=_("Put threshold of sepia, try values in range 80-95"),
    )
    tooltip_if_exists(
        widgets.get("b_bw_run"),
        text=_("Execute only black-white/sepia conversion on current picture"),
    )
    # Contrast
    tooltip_if_exists(
        widgets.get("e1_contrast"), text=_("Black point.\nTry values in range 0-0.2")
    )
    tooltip_if_exists(
        widgets.get("e2_contrast"), text=_("White point.\nTry values in range 0-0.2")
    )
    tooltip_if_exists(
        widgets.get("rb1_contrast"),
        text=_(
            "Enhance contrast of image by adjusting the span of the available colors"
        ),
    )
    tooltip_if_exists(
        widgets.get("rb2_contrast"),
        text=_("Enhances the difference between lighter & darker values of the image"),
    )
    tooltip_if_exists(
        widgets.get("co_contrast_selection"),
        text=_(
            "Select power of reduce (negative values) or increase (positive values) contrast"
        ),
    )
    tooltip_if_exists(
        widgets.get("b_contrast_run"),
        text=_("Execute only change contrast conversion on current picture"),
    )
    # Normalize
    tooltip_if_exists(widgets.get("rb1_normalize"), text=_("Normalize color channels"))
    tooltip_if_exists(
        widgets.get("co_normalize_channel"), text=_("Select channel for normalize")
    )
    tooltip_if_exists(
        widgets.get("rb2_normalize"),
        text=_("Scale the minimum and maximum values to a full quantum range"),
    )
    tooltip_if_exists(
        widgets.get("b_normalize_run"),
        text=_("Execute only color normalize conversion on current picture"),
    )
    # Mirror
    tooltip_if_exists(widgets.get("cb_mirror_flip"), text=_("Mirror top-bottom"))
    tooltip_if_exists(widgets.get("cb_mirror_flop"), text=_("Mirror left-right"))
    tooltip_if_exists(
        widgets.get("b_mirror_run"),
        text=_("Execute only mirror conversion on current picture"),
    )
    # Vignette
    tooltip_if_exists(
        widgets.get("e_vignette_radius"), text=_("Radius of the Gaussian blur effect")
    )
    tooltip_if_exists(
        widgets.get("e_vignette_sigma"),
        text=_("Standard deviation of the Gaussian effect"),
    )
    tooltip_if_exists(
        widgets.get("e_vignette_dx"), text=_("Horizontal offset of vignette")
    )
    tooltip_if_exists(
        widgets.get("e_vignette_dy"), text=_("Vertical offset of vignette")
    )
    tooltip_if_exists(
        widgets.get("l_vignette_color"), text=_("Selected color of corners")
    )
    tooltip_if_exists(
        widgets.get("b_vignette_color"), text=_("Select color of corners")
    )
    tooltip_if_exists(
        widgets.get("b_vignette_run"),
        text=_("Execute only vignette conversion on current picture"),
    )
    # Logo
    tooltip_if_exists(
        widgets.get("b_logo_select"), text=_("Select picture to put on picture")
    )
    tooltip_if_exists(widgets.get("e_logo_width"), text=_("Width picture"))
    tooltip_if_exists(widgets.get("e_logo_height"), text=_("Height picture"))
    tooltip_if_exists(
        widgets.get("e_logo_dx"), text=_("Horizontal offset from gravity point")
    )
    tooltip_if_exists(
        widgets.get("e_logo_dy"), text=_("Vertical offset from gravity point")
    )
    tooltip_if_exists(
        widgets.get("frame_logo_gravity"), text=_("Use gravity for putting picture")
    )
    tooltip_if_exists(
        widgets.get("b_logo_run"), text=_("Execute only add logo on current picture")
    )
    # Compose
    tooltip_if_exists(
        widgets.get("b_compose_select"),
        text=_("Select picture to compose with main picture"),
    )
    tooltip_if_exists(
        widgets.get("rb_compose_bottom"), text=_("Join picture at bottom")
    )
    tooltip_if_exists(widgets.get("rb_compose_right"), text=_("Join picture at right"))
    tooltip_if_exists(
        widgets.get("cb_compose_autoresize"),
        text=_("Autoresize picture if dimensions are not equal"),
    )
    tooltip_if_exists(
        widgets.get("l_compose_color"), text=_("Selected color to fill gap")
    )
    tooltip_if_exists(widgets.get("b_compose_color"), text=_("Select color of gap"))
    tooltip_if_exists(
        widgets.get("rb_compose_N"), text=_("Join picture on right and move to top")
    )
    tooltip_if_exists(
        widgets.get("rb_compose_W"), text=_("Join picture at bottom and move to left")
    )
    tooltip_if_exists(
        widgets.get("rb_compose_C"), text=_("Join picture and move to center")
    )
    tooltip_if_exists(
        widgets.get("rb_compose_E"), text=_("Join picture at bottom and move to right")
    )
    tooltip_if_exists(
        widgets.get("rb_compose_S"), text=_("Join picture on right and move to bottom")
    )
    tooltip_if_exists(
        widgets.get("b_compose_run"),
        text=_("Execute compose picture with current main picture"),
    )
    tooltip_if_exists(
        widgets.get("b_preview_new_run"),
        text=_("Display image to join by IMdisplay or default image viewer of OS"),
    )
