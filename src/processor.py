#!/usr/bin/env python
# coding=utf-8

langset = ['eg', 'th', 'pt']


class line_processor():

    def __init__(self, infile, outfile, lang):
        self.infile = infile
        self.outfile = outfile
        self.lang = lang
        self.operators = []

    def add_operator(self, operators):
        self.operators.append(operators)

    def line_process(self, text):
        for operator in self.operators:
            noerr, text = operator(text, self.lang)
            if not noerr:
                return None
        return text

    def process(self):
        with open(self.infile) as inf, open(self.outfile, 'wb') as of:
            for line in inf:
                text = self.line_process(line.strip())
                if text:
                    of.write(text + '\n')
