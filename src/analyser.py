#!/usr/bin/env python
# coding=utf-8
import when
from collections import defaultdict
from functools import partial

# for debug
import text


class request_type:

    def __init__(self, type_key):
        self.type_key = type_key
        self.total_freq = 0

    def add_query(self, query, query_freq):
        self.total_freq += query_freq


def debug_processor(instance):
    for i in dir(instance):
        print i, getattr(instance, i)


class analyser:

    def __init__(self, lang, text):
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

        self.this_year_freq = 0
        self.last_year_freq = 0
        self.recent_three_month_freq = 0
        self.month_freq_dict = defaultdict(int)
        self.processors = []
        self.main_request_type = None
        self.main_request_degree = 0

    def calc_freq(self):
        # calc month freq
        for query_item in self.query_items:
            self.month_freq_dict[query_item[2]] += int(query_item[1])
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
        for query_item in self.query_items:
            type_key = self.calc_query_type(query_item[0])
            if type_key:
                self.request_types.setdefault(type_key, request_type(type_key))
                self.request_types[type_key].add_query(
                    query_item[0], int(query_item[1]))

    def add_analyze_processor(self, process_func):
        self.processors.append(partial(process_func, instance=self))

    def process(self):
        self.calc_freq()
        for processor in self.processors:
            processor()

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
            return getattr(self, self.lang + '_calc_query_type')(query)

    # TODO
    def th_calc_query_type(self, query):
        return None

    def pt_calc_query_type(self, query):
        return None

    def eg_calc_query_type(self, query):
        return None


ana = analyser('th', text.text)
ana.add_analyze_processor(debug_processor)
ana.process()
