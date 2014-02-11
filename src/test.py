import processor
import logging


#processor = general_processor( 'eg', 'line')
# processor.set_io('log','log2')
# processor.add_operator(operators.line_contain_filter)
# processor.process()
logging.basicConfig(level=logging.INFO)
logging.info('Start')
process = processor.simple_processor_factory('eg', 'line')
process.process('log', 'log2')
