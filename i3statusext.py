#!/usr/bin/env python
# -*- cofing: utf-8 -*-

import sys
import json
from subprocess import Popen, PIPE
from os.path import exists


def get_locked():
    if exists("/tmp/locked"):
        return "X"
    return ""


def get_kb():
    if exists("/home/axel/.i3/kb"):
        with open("/home/axel/.i3/kb") as f:
            return f.readline().rstrip()
    return ""


def get_ram():
    try:
        ram = float(int(Popen(['free', '-m'], stdout=PIPE).communicate()[0].split('\n')[2].split()[2])/1024.0)
        if ram > 6:
            color = "#FF0000"
        elif ram > 4:
            color = "#FFFF00"
        else:
            color = "#00FF00"
        ram = "%.2f" % ram
    except:
        ram = "N/A"
        color = "#FF0000"
    return ram, color


def print_line(message):
    """ Non-buffered printing to stdout. """
    sys.stdout.write(message + '\n')
    sys.stdout.flush()


def read_line():
    """ Interrupted respecting reader for stdin. """
    # try reading a line, removing any extra whitespace
    try:
        line = sys.stdin.readline().strip()
        # i3status sends EOF, or an empty line
        if not line:
            sys.exit(3)
        return line
    # exit on ctrl-c
    except KeyboardInterrupt:
        sys.exit()

if __name__ == '__main__':
    # Skip the first line which contains the version header.
    print_line(read_line())

    # The second line contains the start of the infinite array.
    print_line(read_line())

    while True:
        line, prefix = read_line(), ''
        # ignore comma at start of lines
        if line.startswith(','):
            line, prefix = line[1:], ','

        j = json.loads(line)
        # insert information into the start of the json, but could be anywhere
        j.insert(0, {'full_text': 'KB: %s' % get_kb(), 'name': 'kb'})
        ram_val, ram_col = get_ram()
        j.insert(0, {'full_text': 'RAM: %s/7.5 GB' % ram_val, 'color': ram_col, 'name': 'ram'})
        #j.insert(0, {'full_text': '%s' % get_locked(), 'name': 'gov'})
        # and echo back new encoded json
        print_line(prefix+json.dumps(j))
