#coding=utf-8

def error_format_filter(text,lang):
    if len(text.split('\t')) != 2:
        return False,text
    else:
        return True,text
