from processor import general_processor
import operators


processor = general_processor('log', 'log2', 'eg','block')
processor.add_operator(operators.block_merge_operator)
processor.process()
