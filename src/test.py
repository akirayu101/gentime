from processor import general_processor
import operators


processor = general_processor('intest', 'log', 'eg','line')
processor.add_operator(operators.line_stem_extractor)
processor.add_operator(operators.line_timestamp_operator)
processor.process()
