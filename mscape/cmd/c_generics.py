# //////////////////////////////////////////////////////////////////////////////
# // File:     Name:        c_generics.py                                     //
# //           Language:    Python 3                                          //
# //                                                                          //
# // Details:  This file contains general purpose commands (e.g. clear, etc.) //
# //                                                                          //
# // Author:   Name:    Marijn Verschuren, Ralph Vreman                       //
# //           Email:   marijnverschuren3@gmail.com                           //
# //                                                                          //
# // Date:     2023-10-25                                                     //
# //////////////////////////////////////////////////////////////////////////////

from os import system, name, path

MS_DIR = path.abspath(path.dirname(path.abspath(__file__)) + "/..")

# Command not found handler
def cmd_not_found(ctx):
    if not ctx['cmd_line'].strip() == "":
        print(f"Command \"{ctx['cmd'][0]}\" not found")

# Exit command
def cmd_exit(ctx):
    exit(0)

# Help command
def cmd_help(ctx):
    with open(f'{MS_DIR}/res/help.txt', 'r') as file:
        print(file.read())

# Clear command
def cmd_clear(ctx):
    # Windows
    if name == 'nt':
        _ = system('cls')
 
    # macOS / *nix
    else:
        _ = system('clear')

# Reader offset
def cmd_offset(ctx):
    if len(ctx['cmd']) == 1:
        print("Offset required!")
        return

    ctx['offset'] = int(ctx['cmd'][1], 0)
    print(f"New offset set to {ctx['offset']}")