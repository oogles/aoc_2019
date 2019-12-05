from ..aoc import Puzzle
from .. import intcode


class P(Puzzle):
    
    input_delimiter = ','
    
    def process_input_item(self, input_item):
        
        return int(input_item)
    
    def _part1(self, input_data):
        
        # Update noun and verb, but not for sample data
        if not self.sample:
            input_data[1] = 12
            input_data[2] = 2
        
        return intcode.run_program(input_data)
    
    def _part2(self, input_data):
        
        if self.sample:
            return 'Not operable on sample data'
        
        target_output = 19690720
        
        for noun in range(0, 99):
            for verb in range(0, 99):
                input_data[1] = noun
                input_data[2] = verb
                output = intcode.run_program(input_data)
                
                if output == target_output:
                    return 100 * noun + verb
        else:
            raise Exception('No matching noun/verb found')
