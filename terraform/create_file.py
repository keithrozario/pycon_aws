#!/usr/bin/env python3


"""
Creates files of various sizes, all populated by '1'
files aren't perfectly sized, but good enough
"""

for x in [10, 100, 256, 512, 1024]:
    with open(f'{x}.txt', 'w') as outfile:
        for _ in range(x*1024*1024):
            outfile.write('1')