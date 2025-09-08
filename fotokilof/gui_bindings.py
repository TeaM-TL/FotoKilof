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


def setup_root_bindings(root, actions):
    """
    actions -- dictionary { 'action': function }, function is a callback, called by bind
    """
    if "help_info" in actions:
        root.bind("<F1>", actions["help_info"])
    if "change_theme" in actions:
        root.bind("<F2>", actions["change_theme"])
    if "open_file_prev_key" in actions:
        root.bind("<Prior>", actions["open_file_prev_key"])
    if "open_file_next_key" in actions:
        root.bind("<Next>", actions["open_file_next_key"])
    if "open_file_first_key" in actions:
        root.bind("<Home>", actions["open_file_first_key"])
    if "open_file_last_key" in actions:
        root.bind("<End>", actions["open_file_last_key"])
    if "close_program" in actions:
        root.protocol("WM_DELETE_WINDOW", actions["close_program"])


def setup_widget_bindings(widgets, actions, os_system):
    """
    Connect event into widgets

    widgets -- dictionary { name : widget }
    actions -- dictionary { name : function }
    """
    # Crop: click on preview oryginal
    if "mouse_crop_nw" in actions and "c_preview_orig_pi" in widgets:
        widgets["c_preview_orig_pi"].bind("<Button-1>", actions["mouse_crop_nw"])
    if "mouse_crop_se" in actions and "c_preview_orig_pi" in widgets:
        btn_code = "<Button-2>" if os_system == "MACOS" else "<Button-3>"
        widgets["c_preview_orig_pi"].bind(btn_code, actions["mouse_crop_se"])
    # Preview new picture
    if "preview_new_button" in actions and "c_preview_new_pi" in widgets:
        widgets["c_preview_new_pi"].bind("<Button-1>", actions["preview_new_button"])

    # Combobox
    if "preview_orig_refresh" in actions and "co_preview_selector_orig" in widgets:
        widgets["co_preview_selector_orig"].bind(
            "<<ComboboxSelected>>", actions["preview_orig_refresh"]
        )
    if "preview_new_refresh" in actions and "co_preview_selector_new" in widgets:
        widgets["co_preview_selector_new"].bind(
            "<<ComboboxSelected>>", actions["preview_new_refresh"]
        )
    if (
        "preview_compose_refresh" in actions
        and "co_compose_preview_selector" in widgets
    ):
        widgets["co_compose_preview_selector"].bind(
            "<<ComboboxSelected>>", actions["preview_compose_refresh"]
        )
    if "font_selected" in actions and "co_text_font" in widgets:
        widgets["co_text_font"].bind("<<ComboboxSelected>>", actions["font_selected"])
