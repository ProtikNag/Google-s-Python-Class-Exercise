#!/usr/bin/python
# Copyright 2010 Google Inc.
# Licensed under the Apache License, Version 2.0
# http://www.apache.org/licenses/LICENSE-2.0

# Google's Python Class
# http://code.google.com/edu/languages/google-python-class/

import os
import re
import sys
import urllib.request, urllib.parse, urllib.error

"""Logpuzzle exercise
Given an apache logfile, find the puzzle urls and download the images.

Here's what a puzzle url looks like:
10.254.254.28 - - [06/Aug/2007:00:13:48 -0700] "GET /~foo/puzzle-bar-aaab.jpg HTTP/1.0" 302 528 "-" "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.6) Gecko/20070725 Firefox/2.0.0.6"
"""


def get_url_type(url):
    img_name = url.split('/')[-1]
    splits = img_name.split('-')

    if len(splits) == 2:
        return 'animal'
    else:
        return 'place'


def get_last_name(url):
    return url.split('-')[-1]


def read_urls(filename):
    """Returns a list of the puzzle urls from the given log file,
    extracting the hostname from the filename itself.
    Screens out duplicate urls and returns the urls sorted into
    increasing order."""
    # +++your code here+++

    hostname = filename.split('_')[1]

    urls = []
    with open(filename, 'r') as file:
        for line in file:
            url = re.search('GET\s(\S+)\sHTTP', line).group(1)
            if "/images/puzzle/" in url:
                urls.append('http://' + hostname + url)

    if get_url_type(urls[0]) == 'animal':
        return sorted(list(set(urls)))
    else:
        urls = list(set(urls))
        return sorted(urls, key=get_last_name)


def download_images(img_urls, dest_dir):
    """Given the urls already in the correct order, downloads
    each image into the given directory.
    Gives the images local filenames img0, img1, and so on.
    Creates an index.html in the directory
    with an img tag to show each local image file.
    Creates the directory if necessary.
    """
    # +++your code here+++

    if not os.path.exists(dest_dir):
        os.mkdir(dest_dir)

    img_sources = []
    for i, url in enumerate(img_urls):
        print('Retrieving...', url)
        basename = "img%d" % i
        new_filename = os.path.join(dest_dir, basename)
        img_sources.append(basename)
        urllib.request.urlretrieve(url, new_filename)

    with open(os.path.join(dest_dir, 'index.html'), 'w') as index_file:
        index_file.write("<html><body>\n")
        for src in img_sources:
            index_file.write("<img src=%s>" % src)
        index_file.write("\n</body></html>\n")


def main():
    args = sys.argv[1:]

    if not args:
        print('usage: [--todir dir] logfile ')
        sys.exit(1)

    todir = ''
    if args[0] == '--todir':
        todir = args[1]
        del args[0:2]

    img_urls = read_urls(args[0])

    if todir:
        download_images(img_urls, todir)
    else:
        print('\n'.join(img_urls))


if __name__ == '__main__':
    main()
