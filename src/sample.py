#!/usr/bin/env python
"""
Usage:
      sample.py <infile> <mode>
"""

import random
from docopt import docopt


def get_sample(in_file, mode):
    lines = []
    with open(in_file) as f:
        for line in f:
            lines.append(line)

    lines_num = len(lines)
    sample = [lines[i] for i in random.sample(xrange(1, lines_num), 1000)]
    if mode == "recall":
        for line in sample:
            print '\t'.join(line.strip().split('\t')[:2])
    elif mode == "stem":
        for line in sample:
            print line.strip().split('\t')[0]


if __name__ == "__main__":
    arguments = docopt(__doc__)
    get_sample(arguments['<infile>'], arguments['<mode>'])
