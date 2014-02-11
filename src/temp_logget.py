from querylog_extract import get_querylog_between
import when
times = []
langset = ['eg', 'pt', 'th']

# for i in range(201301,201313):
#    times.append(str(i))
# times.append('201401')
times.append('201402')
times.append('201403')

for lang in langset:
    for i in range(len(times) - 1):
        print times[i] + '01', times[i + 1] + '01', lang, '../data/' + lang + '/' + times[i]
        get_querylog_between(times[i] + '01', times[i + 1]
                             + '01', lang, '../data/' + lang + '/' + times[i])
