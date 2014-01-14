#!/usr/bin/env python
# coding=utf-8

langset = ['eg', 'th', 'pt']


class general_processor():

    def __init__(self, infile, outfile, lang, pro_type):
        self.infile = infile
        self.outfile = outfile
        self.lang = lang
        self.operators = []
        self.pro_type = pro_type

    def add_operator(self, operator):
        if self.pro_type in ['block', 'sh']:
            if len(self.operators):
                print len(self.operators)
                pass  # block and sh processor contain one operator
        # maintain single type in one processor
        if operator.__name__.startswith(self.pro_type):
            self.operators.append(operator)
        else:
            pass  # we need write log here

    # line type process
    def line_process(self, text):
        for operator in self.operators:
            noerr, text = operator(text, self.lang)
            if not noerr:
                return None
        return text

    # analysis_process
    def analysis_process(self, text):
        pass

    def process(self):
        if self.pro_type == 'line':
            with open(self.infile) as inf, open(self.outfile, 'wb') as of:
                for line in inf:
                    text = self.line_process(line.strip())
                    if text:
                        of.write(text + '\n')
        elif self.pro_type in ['block', 'sh']:
            print "in"
            if len(self.operators):
                print "in agin"
                self.operators[0](self.infile, self.outfile)


# simple factory
# filter_process  : all filters, stream based
# shell_process   : using sh command, wrap process apis
# block_process   : sum up datas, etc
# analysis_process: request type analysis, output final data
def simple_processor_factory(instance_type, lang):
    if lang not in langset:
        return None
