# //////////////////////////////////////////////////////////////////////////////
# // File:     Name:        utils.py                                          //
# //           Language:    Python 3                                          //
# //                                                                          //
# // Details:  This file contains important utilties.                         //
# //                                                                          //
# // Author:   Name:    Marijn Verschuren, Ralph Vreman                       //
# //           Email:   marijnverschuren3@gmail.com                           //
# //                                                                          //
# // Date:     2023-10-25                                                     //
# //////////////////////////////////////////////////////////////////////////////

"""
Places a hex character as an ascii character.

This function will ignore non printable console characters.
"""
def put_ascii_chr(c):
    ch = "."

    if (c <= 32) or (c == 127):
        ch = "."
    else:
        ch = chr(c)
    
    print(ch, end = "")

"""
Zero pad a number and return a string of it.
"""
def zpad(num, count, use_hex = False):
    nst = list(hex(num)[2:] if use_hex else str(num))
    nstln = len(nst)

    if nstln > count:
        if use_hex:
            return "F" * count
        else:
            return "0" * count

    for x in range(0, count - nstln):
        nst.insert(0, '0')

    return "".join(nst)

"""
Prints a hex matrix.
"""
def print_hex_matrix(data, show_hdr = True, ascii_view = True, offset_view = True, starting_offset = 0):
    if show_hdr:
        if offset_view:
            print(f"┌{'─' * 8}┬{'─' * 49}┬{'─' * 18}┐")

        print(f"{'│ OFFSET │ ' if offset_view else ''}00 01 02 03 04 05 06 07 08 09 0A 0B 0C 0D 0E 0F {'│ < ASCII REPRST > │' if ascii_view else ''}")
        print(f"{'├────────┼──' if offset_view else '─'}──────────────────────────────────────────────{'─┼──────────────────┤ ' if ascii_view else '─'}")

    # Show matrix
    for x in range(0, len(data)):
        if ((x + 1) % 16 == 1) and offset_view:
            print(f"│ {zpad(starting_offset + x, 6, use_hex = True)} │ ", end = "")

        print(f"{zpad(data[x], 2, use_hex = True)}", end = " ")

        if ascii_view:
            if ((x + 1) % 16 == 0):
                print("│ ", end = "")
                
                # print ascii line
                for x in range(x - 15, x + 1):
                    put_ascii_chr(data[x])

                print(' │')
        else:
            if ((x + 1) % 16 == 0):
                print('')

    # Flush out remainder of the ascii chars
    if ascii_view:
        md = ((x + 1) % 16)
        rem = 16 - md

        #print(f"spaces to fill = {16 - md}")

        if md > 0:
            for y in range(0, rem):
                print("   ", end = "")
            
            print("│ ", end = "")

            for y in range(x - md + 1, x + 1):
                put_ascii_chr(data[y])

            print(f"{' ' * (rem + 1)}│")

    if offset_view:
        print(f"└{'─' * 8}┴{'─' * 49}┴{'─' * 18}┘")