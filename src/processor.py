#!/usr/bin/env python
# coding=utf-8

langset = ['eg', 'th', 'pt']

import operators
import logging


class general_processor():

    def __init__(self, lang, pro_type):
        self.infile = None
        self.outfile = None
        self.lang = lang
        self.operators = []
        self.pro_type = pro_type

    def set_io(self, infile, outfile):
        self.infile = infile
        self.outfile = outfile

    def add_operator(self, operator):
        if self.pro_type in ['block', 'analysis']:
            if len(self.operators):
                logging.warn('type processor contain only one operator')
        if operator.__name__.startswith(self.pro_type):
            self.operators.append(operator)
        else:
            logging.fatal('add operator pro_type not compatible')

    # line type process
    def line_process(self, text, filename):
        for operator in self.operators:
            logging.debug("process %s", operator.__name__)
            logging.debug("text %s", text)
            if operator.__name__ == "line_timestamp_operator":
                noerr, text = operator(
                    text, self.lang, filename.split('/')[-1])
            else:
                noerr, text = operator(text, self.lang)
            if not noerr:
                return None
        return text

    # analysis_process
    def analysis_process(self, text):
        return self.operators[0](text, self.lang)

    def process(self):
        if not self.infile:
            logging.fatal("no input specified")
        if self.pro_type == 'line':
            with open(self.infile) as inf, open(self.outfile, 'ab') as of:
                for line in inf:
                    text = self.line_process(line.strip(), self.infile)
                    if text:
                        of.write(text + '\n')
        elif self.pro_type == 'block':
            if len(self.operators):
                self.operators[0](self.infile, self.outfile)
        elif self.pro_type == 'analysis':
            if len(self.operators):
                with open(self.infile) as inf, open(self.outfile, 'ab') as of:
                    for line in inf:
                        text = self.analysis_process(text)
                        of.write(text + '\n')


class processor_impl():

    def __init__(self, proto_processor):
        self.processor = proto_processor

    def process(self, infile, outfile):
        self.processor.set_io(infile, outfile)
        self.processor.process()

# simple factory
# line_process  : all filters, stream based
# block_process   : sum up datas, etc
# analysis_process: request type analysis, output final data


def simple_processor_factory(lang, instance_type):
    if lang not in langset:
        return None
    proto_processor = general_processor(lang, instance_type)
    if instance_type == 'line':
        proto_processor.add_operator(operators.line_error_format_filter)
        proto_processor.add_operator(operators.line_contain_filter)
        proto_processor.add_operator(operators.line_stem_extractor)
        proto_processor.add_operator(operators.line_timestamp_operator)
    if instance_type == 'block':
        proto_processor.add_operator(operators.block_merge_operator)
    return processor_impl(proto_processor)
