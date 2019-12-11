from ..aoc import Puzzle
from .. import intcode


class P(Puzzle):
    
    input_delimiter = ','
    
    def process_input_item(self, input_item):
        
        return int(input_item)
    
    def _part1(self, input_data):
        
        return intcode.run_program(input_data, [1])
    
    def _part2(self, input_data):
        
        return intcode.run_program(input_data, [2])
