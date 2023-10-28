# //////////////////////////////////////////////////////////////////////////////
# // File:     Name:        main.py                                           //
# //           Language:    Python 3                                          //
# //                                                                          //
# // Details:  Main entry file for memscape.                                  //
# //                                                                          //
# // Author:   Name:    Marijn Verschuren, Ralph Vreman                       //
# //           Email:   marijnverschuren3@gmail.com                           //
# //                                                                          //
# // Date:     2023-10-25                                                     //
# //////////////////////////////////////////////////////////////////////////////

import os
import sys

MOD_DIR = os.path.abspath(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(f"{MOD_DIR}/cmd")

import c_generics
import c_manipl
import c_tools
import c_mmap

# Vars
WORK_DIR = os.path.abspath(os.path.dirname(os.path.abspath(__file__)) + "/../..") + "/work"
DUMP_NAME = "memory.dmp"
DUMP_PATH = f"{WORK_DIR}/dumps/{DUMP_NAME}"

# Context
fd = None # File
cur_addr = 0
fsize = 0
app = {
    'mmap': None
}

# Command List
# --------------------------------
cmd_list = {
    # Basic commands
    'exit': c_generics.cmd_exit,
    'clear': c_generics.cmd_clear,
    'offset': c_generics.cmd_offset,
    'help': c_generics.cmd_help,

    # I/O
    'read': c_manipl.cmd_read,
    'dump': c_manipl.cmd_dump,
    'mmap': c_mmap.cmd_mmap,

    # Utility commands
    'ord': c_tools.cmd_ord
}
# --------------------------------

# Reads the dump
def opendmp():
    global fd
    global fsize
    fd = open(DUMP_PATH, mode="rb")
    fsize = os.path.getsize(DUMP_PATH)
    print("-- ")
    print(f"In Dump: {DUMP_PATH}")
    print(f"Size: {(fsize / 1024 / 1024):.2f} MB")
    print("-- \n")

# Shell loop
def shl():
    global cur_addr

    while True:
        try:
            cmd_line = input(f"{DUMP_NAME} [{hex(cur_addr)}] > ")
            cmd = cmd_line.split(' ')

            # Command context
            context = {
                'fd': fd,
                'fsize': fsize,
                'cmd_line': cmd_line,
                'cmd': cmd,
                'offset': cur_addr,
                'app': app
            }

            # Execute command
            cmd_list.get(cmd[0], c_generics.cmd_not_found)(context)

            # Keep cur address synchronized
            cur_addr = context['offset']
        except Exception as e:
            print(e)

# Entry point
def main():
    print("MemScape 1.0.0")

    if not os.path.exists(DUMP_PATH):
        print("No dump has been made. Please run the dumping tool and rerun the program again.")
        return

    opendmp()
    shl()

main()