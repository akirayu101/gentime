# coding=utf-8

eg_contain_dict = ['احدث', 'الأحدث', 'الاحدث'
                   'السنه', 'العام', 'هذه السنة', 'هذه السنه', 'هذه العام', '2013', '2014']


th_contain_dict = ['ล่าสุด', 'ใหม่ล่าสุด''ใหม่สุด', 'ใหม่ที่สุด'
                   'ปีนี้', '2557', '2014', 'ปี57', 'ปี14', 'ปี2557', 'ปี2014', '2013']

pt_contain_dict = ['mais recente', 'mais recentes'
                   'deste ano', '2014', '2013']

eg_stem_dict = eg_contain_dict
th_stem_dict = th_contain_dict
pt_stem_dict = pt_contain_dict

eg_stem_thresh = 2
th_stem_thresh = 2
pt_stem_thresh = 0

eg_newest_dict = ['احدث', 'الأحدث', 'الاحدث']
th_newest_dict = ['ล่าสุด', 'ใหม่ล่าสุด''ใหม่สุด', 'ใหม่ที่สุด']
pt_newest_dict = ['mais recente', 'mais recentes']

eg_thisyear_dict = ['السنه', 'العام',
                    'هذه السنة', 'هذه السنه', 'هذه العام', '2014']
th_thisyear_dict = ['ปีนี้', '2557', 'ปี57',
                    'ปี14', 'ปี2557', 'ปี2014', '2014']
pt_thisyear_dict = ['deste ano', '2014']

eg_punish_dict = [':']
th_punish_dict = [':']
pt_punish_dict = [':']

pt_stem_min_len = 4
th_stem_min_len = 15
eg_stem_min_len = 15


eg_stem_filter_dict = [
    "اغنيه", "كيفية", "رقص", "اغانى", "طريقة", "كيف", "lyric", "جنس", "مسلسلات", "ديكور", "مهرجانات", "مهرجان", "لعبة",
    "سكس", "mp3", "صور", "برنامج", "حلقة", "العاب", "مسلسل", "اغنية", "فيلم", "اغاني", "فيديوهات", "لعبة", "افلام", "موقع", "فيديو", "تحميل", "نيك"]
pt_stem_filter_dict = ["jogos", "imagens", "mp3",
                       "film", "video", "ouvir", "musica", "facebook", "site"]
th_stem_filter_dict = ["เกม", "เพลง", "หนัง", "คลิป"]
