# //////////////////////////////////////////////////////////////////////////////
# // File:     Name:        c_mmap.py                                         //
# //           Language:    Python 3                                          //
# //                                                                          //
# // Details:  This file contains memory map commands.                        //
# //                                                                          //
# // Author:   Name:    Marijn Verschuren, Ralph Vreman                       //
# //           Email:   marijnverschuren3@gmail.com                           //
# //                                                                          //
# // Date:     2023-10-25                                                     //
# //////////////////////////////////////////////////////////////////////////////

import mmap
import os
import utils
import math

WORK_DIR = os.path.abspath(os.path.dirname(os.path.abspath(__file__)) + "/../..")

"""
Gets a range from the command.
"""
def _get_range(ctx):
    if ctx['app']['mmap'] == None:
        print("Error: no memory map is loaded.")
        return None

    cmdl = len(ctx['cmd'])

    if cmdl < 3:
        print(f"Error: no range id specified")
        return None

    rng_id = ctx['cmd'][2]
    rng = ctx['app']['mmap'].getRange(rng_id)
    
    if rng == None:
        print(f"Error: range does not exist")
        return None

    return { 'rng': rng, 'id': rng_id }

"""
Loads a memory map.
"""
def subcmd_load(ctx):
    cmdl = len(ctx['cmd'])

    if cmdl < 3:
        print(f"Error: no path specified to load.")
        return

    fpath = f"{WORK_DIR}/{ctx['cmd'][2]}"

    if not os.path.exists(fpath):
        print("Error: the specified memory map does not exist.")
        return

    # Prepare mmap
    ctx['app']['mmap'] = mmap.parse(fpath)
    
    print(f'Memory map loaded from "{fpath}"')

"""
Views the currently loaded memory map.
"""
def subcmd_view(ctx):
    if ctx['app']['mmap'] == None:
        print("Error: no memory map is loaded.")
        return

    for g in ctx['app']['mmap'].groups:
        print(g)
        print(f"┌{'─' * 13}┬{'─' * 41}┬{'─' * 14}┬{'─' * 33}┐")
        print(f'│ Id          │ Range                                   │ Size         │ Description                     │ ')
        print(f'├─────────────┼─────────────────────────────────────────┼──────────────┼─────────────────────────────────┤ ')

        ranges = ctx['app']['mmap'].getByGroup(g)
        rangelen = len(ranges)

        for x in range(0, rangelen):
            rng = ranges[x]
            size = rng['_rhs'] - rng['_lhs']
            size_str = ""

            if size > (1024 * 1024): # 1 MiB
                size_str = f"{'{:.2f}'.format(size / 1024 / 1024)} MiB"
            else:
                size_str = f"{'{:.2f}'.format(size / 1024)} KiB"

            # Id
            print(f"│ {rng['id']}{(12 - len(rng['id'])) * ' '}", end = "")

            # Print range
            print(f'│ 0x{utils.zpad(rng["_lhs"], 16, use_hex = True)} - 0x{utils.zpad(rng["_rhs"], 16, use_hex = True)} │ ', end = "")

            # Size calc
            print(f'{size_str}{(13 - len(size_str)) * " "}│ ', end = "")

            # Description
            print(f'{rng["description"]}{(32 - len(rng["description"])) * " "}│')

            if (x + 1) < rangelen:
                print(f'├─────────────┼─────────────────────────────────────────┼──────────────┼─────────────────────────────────┤ ')
        
        print(f"└{'─' * 13}┴{'─' * 41}┴{'─' * 14}┴{'─' * 33}┘")
        print('')

"""
Range read subcommand.
"""
def subcmd_read(ctx):
    arg = _get_range(ctx)

    if arg == None:
        return

    rng = arg['rng']
    fd = ctx['fd']
    fd.seek(rng['_lhs'])
    utils.print_hex_matrix(fd.read(rng['_rhs'] - rng['_lhs']), show_hdr = True, ascii_view = True, offset_view = True, starting_offset = rng['_lhs'])

"""
Range dump subcommand.
"""
def subcmd_dump(ctx):
    RANGE_DIR = os.path.abspath(os.path.dirname(os.path.abspath(__file__)) + "/../../..") + "/work/dumps/ranges"
    
    if not os.path.exists(RANGE_DIR):
        os.mkdir(RANGE_DIR)

    # ---------------------
    
    cmdl = len(ctx['cmd'])

    if cmdl < 4:
        print("Usage: mmap dump <range> <file> - Dumps a range to <file>")
        return

    arg = _get_range(ctx)

    if arg == None:
        return

    rng = arg['rng']
    target = ctx['cmd'][3].strip()
    fd = ctx['fd']

    # Extract segment
    fd.seek(rng['_lhs'])

    with open(f"{RANGE_DIR}/{target}", 'wb') as file:
        file.write(fd.read(rng['_rhs'] - rng['_lhs']))

    print(f"Dump made of '{rng['id']}' with name '{target}'")

# Command list
subcmd_list = {
    'load': subcmd_load,
    'view': subcmd_view,
    'read': subcmd_read,
    'dump': subcmd_dump
}

"""
Sub-command not found handler.
"""
def cmd_not_found(ctx):
    print("invalid subcommand.")

"""
Main MMAP command handler.
"""
def cmd_mmap(ctx):
    cmdl = len(ctx['cmd'])

    if cmdl < 2:
        print(f"Usage: mmap <command> [arguments]\n\
\n\
Valid commands are:\n\
    mmap dump <range> <file>     : Dumps a range to <file>\n\
    load <path>                  : Loads a memory map file.\n\
    read <id>                    : Reads the specified memory range.\n\
    view                         : Views the loaded memory map.\n\
    ")
        return
    
    subcmd_list.get(ctx['cmd'][1], cmd_not_found)(ctx)
