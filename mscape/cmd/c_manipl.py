# //////////////////////////////////////////////////////////////////////////////
# // File:     Name:        c_manipl.py                                       //
# //           Language:    Python 3                                          //
# //                                                                          //
# // Details:  This file contains manipulation commands.                      //
# //                                                                          //
# // Author:   Name:    Marijn Verschuren, Ralph Vreman                       //
# //           Email:   marijnverschuren3@gmail.com                           //
# //                                                                          //
# // Date:     2023-10-25                                                     //
# //////////////////////////////////////////////////////////////////////////////

import utils
import os

"""
Read command
"""
def cmd_read(ctx):
    size = 1
    cmdl = len(ctx['cmd'])

    if cmdl == 1:
        print("Usage: read <offset> [size]")
        return
    elif cmdl > 2:
        size = int(ctx['cmd'][2], 0)

    offset = ctx['offset'] + int(ctx['cmd'][1], 0)
    fd = ctx['fd']
    fd.seek(offset)

    if size == 1:
        val = int(fd.read(1)[0])
        hexVal = hex(val)
        print(f"Value: {hexVal} ({val})")
    else:
        utils.print_hex_matrix(fd.read(size), show_hdr = True, ascii_view = True, offset_view = True, starting_offset = offset)

"""
Dump command
"""
def cmd_dump(ctx):
    SEGS_DIR = os.path.abspath(os.path.dirname(os.path.abspath(__file__)) + "/../../..") + "/work/dumps/segs"
    
    if not os.path.exists(SEGS_DIR):
        os.mkdir(SEGS_DIR)

    # ---------------------
    
    cmdl = len(ctx['cmd'])

    if cmdl < 4:
        print("Usage: dump <offset> <size> <file> - Dumps a range to <file>")
        return

    offset = ctx['offset'] + int(ctx['cmd'][1], 0)
    size = int(ctx['cmd'][2], 0)
    target = ctx['cmd'][3].strip()
    fd = ctx['fd']

    # Extract segment
    fd.seek(offset)

    with open(f"{SEGS_DIR}/{target}", 'wb') as file:
        file.write(fd.read(size))

    print(f"Dump made of {hex(offset)} - {hex(offset + size)} with name '{target}'")