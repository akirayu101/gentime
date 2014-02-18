#!/usr/bin/env python
# coding=utf-8

langset = ['eg', 'th', 'pt']

import operators
import logging
from const import *
import multiprocessing
from itertools import izip
from multiprocessing import Process, Pipe
from functools import partial
import sh


def inner_process(args):
    (infile, outfile, lang, stems, operator) = args
    logging.info('stem recall infile:%s outfile:%s' % (infile, outfile))
    with open(infile) as inf, open(outfile, 'wb') as of:
        for line in inf:
            ok, text = operator(
                line.strip(), lang, stems)
            if ok:
                of.write(text.strip() + '\n')


class general_processor():

    def __init__(self, lang, pro_type):
        self.infile = None
        self.outfile = None
        self.lang = lang
        self.operators = []
        self.pro_type = pro_type
        self.stems = []

    def set_io(self, infile, outfile):
        self.infile = infile
        self.outfile = outfile
        self.cpu_num = multiprocessing.cpu_count()

    def add_operator(self, operator):
        if self.pro_type in ['block', 'analysis', 'stem']:
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

    def inner_process(self, args):
                (infile, outfile) = args
                logging.info('stem recall infile:%s outfile:%s' %
                             (infile, outfile))
                with open(infile) as inf, open(outfile, 'wb') as of:
                    for line in inf:
                        ok, text = self.operators[0](
                            line.strip(), self.lang, self.stems)
                        if ok:
                            of.write(text.strip() + '\n')

    def process(self):
        if not self.infile:
            logging.fatal("no input specified")
        if self.pro_type == 'line':
            with open(self.infile) as inf, open(self.outfile, 'ab') as of, open(mid_datadir + self.lang + '/noquerys_' + file_suffix, 'ab') as noqueryfile:
                for line in inf:
                    text = self.line_process(line.strip(), self.infile)
                    if text:
                        of.write(text + '\n')
                    else:
                        noqueryfile.write(line.strip() + '\n')

        elif self.pro_type in ['block', 'recall']:
            if len(self.operators):
                self.operators[0](self.infile, self.outfile)
        elif self.pro_type == 'analysis':
            if len(self.operators):
                with open(self.infile) as inf, open(self.outfile, 'ab') as of:
                    for line in inf:
                        text = self.analysis_process(line)
                        of.write(text.strip() + '\n')
        elif self.pro_type == 'stem':
            self.load_stem()
            self.open_temps = []
            self.in_files = []
            self.out_files = []
            self.args = []

            for i in xrange(self.cpu_num):
                f = open(mid_datadir + self.lang + '/tempin' + str(i), 'wb')
                self.open_temps.append(f)
                self.in_files.append(
                    mid_datadir + self.lang + '/tempin' + str(i))
                self.out_files.append(
                    mid_datadir + self.lang + '/tempout' + str(i))
            for i in xrange(self.cpu_num):
                self.args.append(
                    (self.in_files[i], self.out_files[i], self.lang, self.stems, self.operators[0]))
            with open(self.infile) as f:
                for i, line in enumerate(f):
                    self.open_temps[i %
                                    self.cpu_num].write(line.strip() + '\n')
            for i in xrange(self.cpu_num):
                self.open_temps[i].close()

            pool = multiprocessing.Pool(self.cpu_num)
            pool.map(inner_process, self.args)
            sh.cat(self.out_files, _out=self.outfile)
            sh.rm('-rf', self.in_files)
            sh.rm('-rf', self.out_files)

    def load_stem(self):
        # load stems
        with open(final_datadir + self.lang + '/stem_' + file_suffix) as stem_file:
            for line in stem_file:
                strength = int(line.strip().split('\t')[2])
                if strength >= 3:
                    self.stems.append(line.strip().split('\t'))


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
        proto_processor.add_operator(operators.line_punish_filter)
        proto_processor.add_operator(operators.line_stem_extractor)
        proto_processor.add_operator(operators.line_timestamp_operator)
    if instance_type == 'block':
        proto_processor.add_operator(operators.block_merge_operator)
    if instance_type == 'analysis':
        proto_processor.add_operator(operators.analysis_stem_operator)
    if instance_type == 'stem':
        proto_processor.add_operator(operators.stem_recall_operator)
    if instance_type == 'recall':
        proto_processor.add_operator(operators.recall_output_operator)
    return processor_impl(proto_processor)
