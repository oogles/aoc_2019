from ..aoc import Puzzle
from .. import intcode


class P(Puzzle):
    
    input_delimiter = ','
    
    def process_input_item(self, input_item):
        
        return int(input_item)
    
    def _part1(self, input_data):
        
        # One manual input required: the ID of the air conditioning system, to
        # be tested by the diagnostic program (the puzzle input)
        if not self.sample:
            manual_inputs = [1]
        else:
            manual_inputs = None
        
        return intcode.run_program(input_data, manual_inputs)
    
    def _part2(self, input_data):
        
        # One manual input required: the ID of the thermal radiator controller,
        # to be tested by the diagnostic program (the puzzle input)
        if not self.sample:
            manual_inputs = [5]
        else:
            manual_inputs = None
        
        return intcode.run_program(input_data, manual_inputs)
