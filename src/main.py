import processor
import logging
import sh
import when
import re
from const import *

langset = ['eg', 'th', 'pt']
#langset = ['pt']

logging.basicConfig(
    format='%(levelname)s %(asctime)s %(message)s', level=logging.INFO)


def file_names(DIR):
    return re.split('\t|\n', str(sh.ls(DIR).strip()))


def clean_mid_data():
    stepnames = ['step' + str(i) + '_' + file_suffix for i in range(1, 5)]
    for lang in langset:
        for stepname in stepnames:
            sh.rm('-rf', mid_datadir + lang + '/' + stepname)
        sh.rm('-rf', mid_datadir + lang + '/' + 'noquerys_' + file_suffix)


def clean_final_data():
    for lang in langset:
        sh.rm('-rf', final_datadir + lang + '/' + 'stem_' + file_suffix)


def step1():
    logging.info('Step 1: processing raw data')
    for lang in langset:
        process = processor.simple_processor_factory(lang, 'line')
        files = file_names(datadir + lang)
        for f in files:
            logging.info('Step 1:  processing lang:%s file:%s', lang, f)
            process.process(datadir + lang + '/' + f, mid_datadir +
                            lang + '/' + 'step1_' + file_suffix)


def step2():
    for lang in langset:
        logging.info('Step 2:  processing lang:%s', lang)
        process = processor.simple_processor_factory(lang, 'block')
        process.process(mid_datadir + lang + '/' + 'step1_' + file_suffix,
                        mid_datadir + lang + '/' + 'step2_' + file_suffix)


def step3():
    for lang in langset:
            logging.info('Step 3: calc stem lang:%s', lang)
            process = processor.simple_processor_factory(lang, 'analysis')
            process.process(mid_datadir + lang + '/' + 'step2_' + file_suffix,
                            mid_datadir + lang + '/' + 'step3_' + file_suffix)


def step4():
    for lang in langset:
            logging.info('Step 4: stem recall lang:%s', lang)
            process = processor.simple_processor_factory(lang, 'stem')
            process.process(
                mid_datadir + lang + '/' + 'noquerys_' + file_suffix,
                mid_datadir + lang + '/' + 'step4_' + file_suffix)


def step5():
    for lang in langset:
            logging.info('Step 5: recall calc lang:%s', lang)
            process = processor.simple_processor_factory(lang, 'recall')
            process.process(
                mid_datadir + lang + '/' + 'step4_' + file_suffix,
                mid_datadir + lang + '/' + 'step5_' + file_suffix)


def main():
    clean_mid_data()
    clean_final_data()
    logging.info('Start processing')
    step1()
    step2()
    step3()
    step4()
    step5()

if __name__ == "__main__":
    main()
