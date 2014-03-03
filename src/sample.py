#!/usr/bin/env python
"""
Usage:
      sample.py <infile> <outfile> <mode>
"""

import random
from docopt import docopt
import xlwt


def get_sample(in_file, out_file, mode):
    lines = []
    with open(in_file) as f:
        for line in f:
            lines.append(line)

    lines_num = len(lines)
    sample = [lines[i] for i in random.sample(xrange(1, lines_num), 1000)]
    sample = [i.strip().split('\t') for i in sample]

    querys = map(lambda x: x[0], sample)
    querys = ["query"] + querys
    query_type = map(lambda x: x[1], sample)
    query_type = ["gentype"] + query_type

    if mode == "recall":
        book_value = [querys, query_type]
        xls = xlwt.Workbook(encoding="UTF-8")
        sheet = xls.add_sheet("gentype")
        for i in range(len(book_value)):
            for j in range(len(book_value[0])):
                sheet.write(j, i, book_value[i][j])
        xls.save(out_file)

    elif mode == "stem":
        book_value = [querys]
        xls = xlwt.Workbook(encoding="UTF-8")
        sheet = xls.add_sheet("querys")
        for i in range(len(book_value)):
            for j in range(len(book_value[0])):
                sheet.write(j, i, book_value[i][j])
        xls.save(out_file)


if __name__ == "__main__":
    arguments = docopt(__doc__)
    print arguments
    get_sample(arguments['<infile>'],
               arguments['<outfile>'], arguments['<mode>'])
