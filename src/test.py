from processor import line_processor
import operators


processor = line_processor('intest', 'log', 'eg')
processor.add_operator(operators.stem_extractor)
processor.add_operator(operators.timestamp_operator)
processor.process()
