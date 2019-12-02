from . import AdventOfCode
from . import intcode


class Day(AdventOfCode):
    
    day = 2
    
    process_as_list = False
    
    def _get_input_data(self, input_data):
        
        return [int(i) for i in input_data.split(',')]
    
    def _part1(self, input_data):
        
        input_data[1] = 12
        input_data[2] = 2
        
        return intcode.run_program(input_data)
    
    def _part2(self, input_data):
        
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


if __name__ == '__main__':
    Day(test=False).solve()
