import processor
import logging
import sh
import when
import re
from const import *

langset = ['eg', 'th', 'pt']
file_suffix = when.now().strftime("%Y%m%d")
logging.basicConfig(
    format='%(levelname)s %(asctime)s %(message)s', level=logging.INFO)


def file_names(DIR):
    return re.split('\t|\n', str(sh.ls(DIR).strip()))


def clean_mid_data():
    stepnames = ['step' + str(i) + '_' + file_suffix for i in range(1, 5)]
    for lang in langset:
        for stepname in stepnames:
            sh.rm('-rf', mid_datadir + lang + '/' + stepname)


def main():
    clean_mid_data()

    logging.info('Start processing')
    logging.info('Step 1: processing raw data')
    # step1 processing raw data
    for lang in langset:
        process = processor.simple_processor_factory(lang, 'line')
        files = file_names(datadir + lang)
        for f in files:
            logging.info('Step 1:  processing lang:%s file:%s', lang, f)
            process.process(datadir + lang + '/' + f, mid_datadir +
                            lang + '/' + 'step1_' + file_suffix)
    # step2 merging raw data
    for lang in langset:

        logging.info('Step 2:  processing lang:%s', lang)
        process = processor.simple_processor_factory(lang, 'block')
        process.process(mid_datadir + lang + '/' + 'step1_' + file_suffix,
                        mid_datadir + lang + '/' + 'step2_' + file_suffix)
    # step3 calc stem type and strengh
    if 1:
        for lang in langset:
            logging.info('Step 3: calc stem ,lang:%s', lang)
            process = processor.simple_processor_factory(lang, 'analysis')
            process.process(mid_datadir + lang + '/' + 'step2_' + file_suffix,
                            mid_datadir + lang + '/' + 'step3_' + file_suffix)


if __name__ == "__main__":
    main()
