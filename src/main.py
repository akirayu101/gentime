import processor
import logging
import sh
import when
import re

langset = ['eg', 'th', 'pt']
datadir = '../data/'
mid_datadir = '../mid_data/'
file_suffix = when.now().strftime("%Y%m%d")

def file_names(DIR):
    return re.split('\t|\n',str(sh.ls(DIR).strip()))


def main():
    logging.basicConfig(level=logging.INFO)
    logging.info('Start processing')
    logging.info('Step 1: processing raw data')
    process = processor.simple_processor_factory('eg', 'line')
    for lang in langset:
        files = file_names(datadir+lang)
        for f in files:
            logging.info('Step 1:  processing lang:%s file:%s', lang, f)
            process.process(datadir+lang+'/'+f,mid_datadir+lang+'/'+'step1_'+file_suffix)

if __name__ == "__main__" :
    main()
