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


- out_full_filename - prepare output file for conversion
"""
import os

import log


def out_full_filename(file_in, destination, extension):
    """
    Input:
        file_in - original file for processing
        destination - output directory
        extension - extension of result file, for change format (jpg->png)
    Output:
        file_out - fullname file for processing in destination
    """
    result = "OK"  # initial value
    if file_in is not None:
        if os.path.isfile(file_in):
            # making output diretory if not exist
            out_dir = os.path.join(os.path.dirname(file_in), destination)
            if os.path.isdir(out_dir) is False:
                try:
                    os.mkdir(out_dir)
                except FileExistsError:
                    log.write_log("pre_imagick: FileExistsError" + out_dir, "E")
                except FileNotFoundError:
                    try:
                        os.mkdir(os.path.dirname(out_dir))
                    except FileNotFoundError:
                        log.write_log("pre_imagick: Cannot make directory for output pictures" + os.path.dirname(out_dir), "E")
                        result = None
                    except:
                        log.write_log("pre_imagick: other problem to create" + os.path.dirname(out_dir), "E")
                        result = None
                    if result == "OK":
                        try:
                            os.mkdir(out_dir)
                        except FileExistsError:
                            log.write_log("pre_imagick: FileExistsError" + out_dir, "E")
                        except FileNotFoundError:
                            log.write_log("pre_imagick: FileExistsError" + os.path.dirname(out_dir), "E")
                            result = None
                        except:
                            log.write_log("pre_imagick: other problem to create" + out_dir, "E")
                            result = None
                except:
                    log.write_log("pre_imagick: other problem to create" + out_dir, "E")
                    result = None

        else:
            result = None
    else:
        result = None

    if result == "OK":
        # preparing output filename
        file_in_without_ext = os.path.splitext(file_in)
        file_out = os.path.join(out_dir,
                                os.path.basename(file_in_without_ext[0] \
                                                 + extension))
    else:
        file_out = None
    return file_out

# EOF
