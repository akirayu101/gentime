#coding=utf-8
import process_dict

def error_format_filter(text,lang):
    if len(text.split('\t')) != 2:
        return False,text
    else:
        return True,text

def contain_filter(text,lang):
    contain_dict = getattr(process_dict,lang+'_contain_dict')
    print contain_dict

    for contain_seg in contain_dict:
        if contain_seg in text.split('\t')[0]:
            return True,text
    return False,text
