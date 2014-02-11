#!/usr/bin/env python
# coding=utf-8

langset = ['eg', 'th', 'pt']

import operators
import logging
logging.basicConfig(level=logging.INFO)


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
        if self.pro_type in ['block', 'sh']:
            if len(self.operators):
                logging.warn('type processor contain only one operator')
                pass
        if operator.__name__.startswith(self.pro_type):
            self.operators.append(operator)
        else:
            pass  # we need write log here

    # line type process
    def line_process(self, text):
        for operator in self.operators:
            logging.debug("process %s", operator.__name__)
            noerr, text = operator(text, self.lang)
            if not noerr:
                return None
        return text

    # analysis_process
    def analysis_process(self, text):
        pass

    def process(self):
        if not self.infile:
            logging.fatal("no input specified")
        if self.pro_type == 'line':
            with open(self.infile) as inf, open(self.outfile, 'wb') as of:
                for line in inf:
                    text = self.line_process(line.strip())
                    if text:
                        of.write(text + '\n')
        elif self.pro_type in ['block', 'sh']:
            if len(self.operators):
                self.operators[0](self.infile, self.outfile)


class processor_impl():

    def __init__(self, proto_processor):
        self.processor = proto_processor

    def process(self, infile, outfile):
        self.processor.set_io(infile, outfile)
        self.processor.process()

# simple factory
# filter_process  : all filters, stream based
# shell_process   : using sh command, wrap process apis
# block_process   : sum up datas, etc
# analysis_process: request type analysis, output final data


def simple_processor_factory(lang, instance_type):
    if lang not in langset:
        return None
    proto_processor = general_processor(lang, instance_type)
    if instance_type == 'line':
        proto_processor.add_operator(operators.line_error_format_filter)
        proto_processor.add_operator(operators.line_contain_filter)
    return processor_impl(proto_processor)
