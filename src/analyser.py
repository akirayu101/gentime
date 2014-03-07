#!/usr/bin/env python
# coding=utf-8
import when
from collections import defaultdict
from functools import partial
import process_dict
from const import *
import logging

# for debug
#import text


class request_type:

    def __init__(self, type_key):
        self.type_key = type_key
        self.freq = 0
        self.querys = {}

    def add_query(self, query, query_freq):
        self.freq += query_freq
        self.querys.setdefault(query, 0)
        self.querys[query] += query_freq


class analyser:

    def __init__(self, text, lang):
        self.lang = lang
        self.stem = text.strip().split('\t')[0]

        # [[query, freq, timestamp]]
        self.query_items = map(
            lambda t: t.strip().split(':'), text.strip().split('\t')[1:])
        self.querys = [item[0] for item in self.query_items]
        self.querys = list(set(self.querys))

        self.this_year = when.past(years=0).strftime("%Y")
        self.last_year = when.past(years=1).strftime("%Y")
        self.next_year = when.future(years=1).strftime("%Y")
        self.year_before_last = when.past(years=2).strftime("%Y")

        self.recent_three_month = [
            self.month_name_helper(i) for i in xrange(3)]

        self.total_freq = 0
        self.this_year_freq = 0
        self.last_year_freq = 0
        self.recent_three_month_freq = 0
        self.month_freq_dict = defaultdict(int)
        self.processors = []
        self.main_request_type = None
        self.main_request_degree = 0
        for i in dir(self):
            if i.startswith('general_processor'):
                self.add_analyze_processor(getattr(self, i))
        for i in dir(self):
            if i.startswith(self.lang + '_processor'):
                self.add_analyze_processor(getattr(self, i))

    # general_processor starts here
    def nogeneral_processor_debug(self):
        for i in dir(self):
            print i, getattr(self, i)

    def general_processor_calc_freq(self):
        # calc month freq
        for query_item in self.query_items:
            self.month_freq_dict[query_item[2]] += int(query_item[1])
            self.total_freq += int(query_item[1])
        for month_name, freq in self.month_freq_dict.items():
            if self.this_year in month_name:
                if month_name in self.recent_three_month:
                    self.recent_three_month_freq += freq
                self.this_year_freq += freq
            elif self.last_year in month_name:
                self.last_year_freq += freq
            else:
                pass

        self.request_types = {}
        self.request_types.setdefault('newest', request_type('newest'))
        for query_item in self.query_items:
            type_key = self.calc_query_type(query_item[0])
            if type_key:
                self.request_types.setdefault(type_key, request_type(type_key))
                self.request_types[type_key].add_query(
                    query_item[0], int(query_item[1]))

    def add_analyze_processor(self, process_func):
        self.processors.append(process_func)

    def process(self):
        for processor in self.processors:
            processor()
        return self.gen_output()

    def month_name_helper(self, i):
        return when.past(months=i).strftime('%Y%m')

    def calc_query_type(self, query):
        if self.this_year in query:
            return self.this_year
        elif self.last_year in query:
            return self.last_year
        elif self.year_before_last in query:
            return self.year_before_last
        elif self.next_year in query:
            return self.next_year
        else:
            return self.calc_query_type(query)

    def calc_query_type(self, query):
        newest_dict = getattr(process_dict, self.lang + '_newest_dict')
        for word in newest_dict:
            if word in query:
                return 'newest'
        thisyear_dict = getattr(process_dict, self.lang + '_thisyear_dict')
        for word in thisyear_dict:
            if word in query:
                return self.this_year
        if self.last_year in query:
                return self.last_year
        return 'year'

    # TODO
    def gen_output(self):
        # first we calc stem type
        this_year_type = 'year'
        newest_type = 'newest'
        giventime_type = 'given'
        stem_type = 'undefined'
        stem_strength = 0
        if float(self.request_types['newest'].freq) / self.total_freq >= 0.3:
            stem_type = newest_type
        else:
            if float(self.recent_three_month_freq) / self.total_freq >= 0.3:
                stem_type = newest_type
            else:
                stem_type = this_year_type
        # then we calc strength
        if self.total_freq > 10:
            stem_strength = 3
        elif self.total_freq > 5:
            stem_strength = 2
        else:
            stem_strength = 1

        # here we write to stem file
        if not filter_stem(self.stem, self.lang) and stem_strength > getattr(process_dict, self.lang + "_stem_thresh"):
            with open(final_datadir + self.lang + '/' + 'stem_' + file_suffix, 'ab') as f:
                f.write(
                    '\t'.join([self.stem, stem_type, str(stem_strength)]) + '\n')

        ret = ''
        for k, request in self.request_types.items():
            for query, freq in request.querys.items():
                if freq > 10:
                    ret += '\t'.join([query, k, '3']) + '\n'
                elif freq > 5:
                    ret += '\t'.join([query, k, '2']) + '\n'
                else:
                    ret += '\t'.join([query, k, '1']) + '\n'
        return ret


#ana = analyser('pt', text.text)
# ana.add_analyze_processor(debug_processor)
# print ana.process()
def filter_stem(stem, lang):
    if len(stem) < 4:
        return True
    elif 'www' in stem:
        return True
    elif '.com' in stem:
        return True
    elif len(stem.strip().split(' ')) == 1 and stem.strip().isalpha():
        return True
    elif len(stem.strip()) < getattr(process_dict, lang + "_stem_min_len"):
        return True
    elif len(stem.strip()) > 128:
        return True
    else:
        stem_filter_words = getattr(process_dict, lang + "_stem_filter_dict")
        for word in stem_filter_words:
            if word in stem:
                return True
        return False
