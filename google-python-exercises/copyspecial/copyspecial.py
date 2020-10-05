#!/usr/bin/python
# Copyright 2010 Google Inc.
# Licensed under the Apache License, Version 2.0
# http://www.apache.org/licenses/LICENSE-2.0

# Google's Python Class
# http://code.google.com/edu/languages/google-python-class/

import sys
import re
import os
import shutil
import subprocess

"""Copy Special exercise
"""


# +++your code here+++
# Write functions and modify main() to call them


def get_special_paths(dir):
    files = os.listdir(dir)
    special_paths = []

    for f in files:
        search = re.search('__\w+__', f)
        if search != None:
            path = os.path.abspath(f)
            special_paths.append(path)

    return special_paths


def copy_to(paths, dir):
    if not os.path.exists(dir):
        os.mkdir(dir)
    for path in paths:
        filename = os.path.basename(path)
        shutil.copy(path, os.path.join(dir, filename))


def remove_space_from_directory_name(paths):
    new_paths = []
    for path in paths:
        last_path = ""
        for char in path:
            if char == ' ' or char == '\'':
                last_path += '\\'
            last_path += char
        new_paths.append(last_path)

    return new_paths


def zip_to(paths, zippath):
    paths = remove_space_from_directory_name(paths)
    command = 'zip -j ' + zippath + ' ' + ' '.join(paths)
    print("Command I'm going to do:", command)

    if not os.path.exists(os.path.dirname(zippath)):
        os.mkdir(os.path.dirname(zippath))

    (status, output) = subprocess.getstatusoutput(command)
    if status:
        sys.stderr.write(output)
        sys.exit(1)


def main():
    # This basic command line argument parsing code is provided.
    # Add code to call your functions below.

    # Make a list of command line arguments, omitting the [0] element
    # which is the script itself.
    args = sys.argv[1:]
    if not args:
        print("usage: [--todir dir][--tozip zipfile] dir [dir ...]");
        sys.exit(1)
    # todir and tozip are either set from command line
    # or left as the empty string.
    # The args array is left just containing the dirs.
    todir = ''
    if args[0] == '--todir':
        todir = args[1]
        del args[0:2]

    tozip = ''
    if args[0] == '--tozip':
        tozip = args[1]
        del args[0:2]

    if len(args) == 0:
        print("error: must specify one or more dirs")
        sys.exit(1)

    special_files = []
    for dirname in args:
        special_files.extend(get_special_paths(dirname))

    if todir:
        copy_to(special_files, todir)
    elif tozip:
        zip_to(special_files, tozip)
    else:
        print('\n'.join(special_files))

    # +++your code here+++
    # Call your functions


if __name__ == "__main__":
    main()
