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
    return re.split('\t|\n', str(sh.ls(DIR).strip()))


def main():
    logging.basicConfig(level=logging.INFO)
    logging.info('Start processing')

    # clean error file
    stepnames = ['step' + str(i) + '_' + file_suffix for i in range(1, 5)]
    for lang in langset:
        for stepname in stepnames:
            sh.rm('-rf', mid_datadir + lang + '/' + stepname)

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


if __name__ == "__main__":
    main()
