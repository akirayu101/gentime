#!/usr/bin/env python
"""
Usage:
      sample.py <infile>
"""

import random
from docopt import docopt


def get_sample(in_file):
    lines = []
    with open(in_file) as f:
        for line in f:
            lines.append(line)

    lines_num = len(lines)
    sample = [lines[i] for i in random.sample(xrange(1, lines_num), 1000)]
    for line in sample:
        print '\t'.join(line.strip().split('\t')[:2])


if __name__ == "__main__":
    arguments = docopt(__doc__)
    get_sample(arguments['<infile>'])
