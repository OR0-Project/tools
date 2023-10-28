# //////////////////////////////////////////////////////////////////////////////
# // File:     Name:        c_tools.py                                        //
# //           Language:    Python 3                                          //
# //                                                                          //
# // Details:  This file contains tool commands.                              //
# //                                                                          //
# // Author:   Name:    Marijn Verschuren, Ralph Vreman                       //
# //           Email:   marijnverschuren3@gmail.com                           //
# //                                                                          //
# // Date:     2023-10-25                                                     //
# //////////////////////////////////////////////////////////////////////////////

import utils

# Ord command
def cmd_ord(ctx):
    if len(ctx['cmd']) == 1:
        print("Character required!")
        return

    fullIn = ctx['cmd_line'][4:]
    slen = len(fullIn)

    if slen == 1:
        val = ord(ctx['cmd'][1][0])
        print(f"Char Code: {hex(val)} ({val})")
    else:
        utils.print_hex_matrix(list(map(ord, fullIn)), show_hdr = True, ascii_view = False, offset_view = False)
        print('\n')