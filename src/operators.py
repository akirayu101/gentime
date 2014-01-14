# coding=utf-8
import process_dict
import re
import when
import sh

# 过滤器operator
# 返回bool
# in  query freq
# out query freq


def line_error_format_filter(text, lang):
    if len(text.split('\t')) == 2:
        try:
            seg = text.strip().split('\t')
            query = str(seg[0])
            freq = int(seg[1])
            return True, text
        except ValueError:
            return False, text
    else:
        return False, text


def line_contain_filter(text, lang):
    contain_dict = getattr(process_dict, lang + '_contain_dict')
    for contain_seg in contain_dict:
        if contain_seg in text.split('\t')[0]:
            return True, text
    return False, text


def line_punish_filter(text, lang):
    punish_dict = getattr(process_dict, lang + '_punish_dict')
    for punish_seg in punish_dict:
        if punish_seg in text.split('\t')[0]:
            return False, text
    return True, text


def line_prefix_filter(text, lang):
    prefix_dict = getattr(process_dict, lang + '_prefix_dict')
    for prefix_seg in prefix_dict:
        if text.split('\t')[0].startswith(prefix_seg):
            return True, text
    return False, text


# 主干提取operator
# 全返回true和text

# in  query \t freq
# out stem \t query \t freq

def line_stem_extractor(text, lang):
    stem_dict = getattr(process_dict, lang + '_stem_dict')
    [query, freq] = text.strip().split('\t')
    for stem in stem_dict:
        stem_index = query.find(stem)
        if stem_index != -1:
            stem_query = query[:stem_index] + query[stem_index + len(stem):]
            return True, '\t'.join([stem_query, query, freq])
    # almost impossible to reach here
    return False, text

# 替换stem

# in  oldstem \t query \t freq
# out newstem \t query \t freq


def line_sed_operator(text, lang):
    sed_dict = getattr(process_dict, lang + '_sed_dict')
    # dict key: sub_pattern value: replace_term

    [stem_query, query, freq] = text.strip().split('\t')
    for sed in sed_dict:
        sed_compiler = re.compile(sed)
        if sed_compiler.search(stem_query):
            stem_query = sed_compiler.sub(sed_dict[sed], stem_query)
            return True, '\t'.join([stem_query, query, freq])
    return True, text

# add timestamp

# in  stem query freq
# out stem query freq time(exmple 201401)


def line_timestamp_operator(text, lang):
    [stem_query, query, freq] = text.strip().split('\t')
    timestamp = when.now().strftime("%Y%m")
    return True, '\t'.join([stem_query, query, freq, timestamp])

# sh function start with sh prefix


# block function start with block
# block merge operator
# in  stem query freq time
# out stem [query:freq:time]
def block_merge_operator(infile, outfile):
    stem_dict = {}
    with open(infile) as inf, open(outfile, 'wb') as of:
        for line in inf:
            text = line.strip().split('\t')
            [stem, item] = [text[0], text[1:]]
            if stem not in stem_dict:
                stem_dict.setdefault(stem, [])
            else:
                stem_dict[stem].append(':'.join(item))
        for key in stem_dict:
            of.write(key + '\t' + '\t'.join(stem_dict[key]) + '\n')
