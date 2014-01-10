#coding=utf-8
import process_dict

def error_format_filter(text,lang):
    if len(text.split('\t')) != 2:
        return False,text
    else:
        return True,text

def contain_filter(text,lang):
    contain_dict = getattr(process_dict,lang+'_contain_dict')
    for contain_seg in contain_dict:
        if contain_seg in text.split('\t')[0]:
            return True,text
    return False,text

def punish_filter(text,lang):
    punish_dict = getattr(process_dict,lang+'_punish_dict')
    for punish_seg in punish_dict:
        if punish_seg in text.split('\t')[0]:
            return False,text
    return True,text

def prefix_filter(text,lang):
    prefix_dict = getattr(process_dict,lang+'_prefix_dict')
    for prefix_seg in prefix_dict:
        if text.split('\t')[0].startswith(prefix_seg):
            return True,text
    return False,text
