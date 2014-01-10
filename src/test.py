from processor import line_processor
import operators



processor = line_processor('test','log','th')
processor.add_operator(operators.error_format_filter)
processor.process()
