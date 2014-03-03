#!/usr/bin/env python
"""
Usage:
      cover_calc.py <indir> <infile>
"""

import sh
import collections
from docopt import docopt


def cover_calc(in_dir, infile):
    all_query_files = sh.ls(in_dir).split()
    all_query_files = [in_dir + "/" + i for i in all_query_files]

    query_dict = collections.defaultdict(int)
    gentime_query_dict = collections.defaultdict(int)

    for fname in all_query_files:
        print "processing", fname
        with open(fname) as f:
            for line in f:
                try:
                    (query, freq) = line.strip().split('\t')
                    query_dict[query] += int(freq)
                except ValueError:
                    pass
    with open(infile) as f:
        for line in f:
            query = line.strip().split('\t')[0]
            gentime_query_dict[query] = query_dict[query]

    total = 0
    gen_freq = 0

    for k in query_dict:
        total += query_dict[k]
    for k in gentime_query_dict:
        gen_freq += gentime_query_dict[k]

    print gen_freq, total, float(gen_freq) / total


if __name__ == "__main__":
    arguments = docopt(__doc__)
    cover_calc(arguments['<indir>'], arguments['<infile>'])
