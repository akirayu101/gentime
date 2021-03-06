import when
datadir = '../data/'
mid_datadir = '../mid_data/'
final_datadir = '../final_data/'
dict_dir = '../dict/'
file_suffix = when.now().strftime("%Y%m%d")
newest_time = when.past(0, 3).strftime("%Y%m%d")

gentime_type = {'year': ['1', '0'], 'newest': ['3', newest_time],
                '2014': ['2', '0'], '2013': ['3', '20130101']}
