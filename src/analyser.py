#!/usr/bin/env python
# coding=utf-8
import when
from collections import defaultdict

# for debug
import text


class request_type:

    def __init__(self, type_key):
        self.type_key = type_key
        self.querys = []
        self.total_freq = 0

    def add_query(query, query_freq):
        self.querys.append(query)
        self.total_freq += query_freq


class analyser:

    def __init__(self, lang, text):
        self.lang = lang
        self.stem = text.strip().split('\t')[0]

        # [[query, freq, timestamp]]
        self.query_items = map(
            lambda t: t.strip().split(':'), text.strip().split('\t')[1:])
        self.querys = [item[0] for item in self.query_items]

        self.this_year = when.past(years=0).strftime("%Y")
        self.last_year = when.past(years=1).strftime("%Y")
        self.next_year = when.future(years=1).strftime("%Y")
        self.year_before_last = when.past(years=2).strftime("%Y")
        self.month_freq_dict = defaultdict(int)
        for query_item in self.query_items:
            self.month_freq_dict[query_item[2]] += int(query_item[1])

    def debug_log(self):
        for i in dir(self):
            print i, getattr(self, i)


ana = analyser('chn', text.text)
ana.debug_log()
