# Source lines of code counter

import os
import sys
import json

project = None
WORK_DIR = os.path.abspath(os.path.dirname(os.path.abspath(__file__)) + "/..")

with open(WORK_DIR + "/tools/sloc_projects.json", 'r') as file:
    sloc_projects = json.load(file)

# Processes a project
def count_sloc(path):
    stats = {}

    for root, dirs, files in os.walk(path):
        for f in files:
            fPath = os.path.join(root, f)
            ext = os.path.splitext(fPath)[1]

            # ignore non specified file
            if not ext in project['extensions']:
                continue

            # Create stats object if it doesnt exist
            if not ext in stats:
                stats[ext] = {
                    'files': 0,
                    'lines': 0
                }

            stats[ext]['files'] += 1
            
            # Read file and get count
            with open(fPath, 'r') as fd:
                stats[ext]['lines'] += len(fd.readlines())

    return stats

# Show sloc details
def interpret_sloc(stats):
    total_files = 0
    total_lines = 0
    statKeys = stats.keys()

    print(" -- files --")
    
    for ext in statKeys:
        total_files += stats[ext]['files']
        total_lines += stats[ext]['lines']

        print(f"[{ext}]:")
        print(f" Files: {stats[ext]['files']}")
        print(f" Lines: {stats[ext]['lines']}")
        print("")

    print(" -- totals -- ")
    print("Total Files = " + str(total_files))
    print("Total Lines = " + str(total_lines))

# Entry point
def main():
    global project

    # check if project arg is specified
    if len(sys.argv) == 1:
        print("error: no project specified to run sloc for.\n")
        print("available projects are:")

        for proj in sloc_projects:
            print(" - " + proj['name'])

        exit(1)

    # locate project
    for proj in sloc_projects:
        if proj['name'] == sys.argv[1]:
            project = proj

    if project == None:
        print("error: project not found.")
        exit(1)

    # check project
    resolvedPath = os.path.abspath(os.path.join(WORK_DIR, proj['path']))

    if os.path.exists(resolvedPath) and os.path.isdir(resolvedPath):
        interpret_sloc(count_sloc(resolvedPath))
    else:
        print("error: project dir does not exist.")
        exit(1)

main()