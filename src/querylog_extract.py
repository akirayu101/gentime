import sh
cmd = '''"SELECT normalized_query AS normalized_query ,COUNT(CASE WHEN action_name = 'se' AND page_no = 1 AND (rsv_map IS NULL OR COALESCE(rsv_map['rsv_sugtype'],'-')!='cr') THEN 1 ELSE NULL END)  AS search_num FROM default.ud_ml_gps_click_theme WHERE partition_stat_date >= %s AND partition_stat_date <= %s AND partition_stat_language=%s AND IF(COALESCE(rsv_map['rsv_sugtype'],'-')!='cr','0','1')='0' GROUP BY normalized_query SORT BY search_num DESC LIMIT 600000 "'''

lang_dict = {'eg': "'ar-EG'", 'th': "'th-TH'", "pt": "'pt-BR'"}


def get_querylog_between(start, end, lang, outfile):
    current_cmd = cmd % (repr(start), repr(end), lang_dict[lang])
    print current_cmd
    sh.queryengine('-e', current_cmd, _out=outfile, _err='error.log')
