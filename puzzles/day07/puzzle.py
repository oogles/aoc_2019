import itertools

from ..aoc import Puzzle
from .. import intcode


class P(Puzzle):
    
    input_delimiter = ','
    
    def process_input_item(self, input_item):
        
        return int(input_item)
    
    def _part1(self, input_data):
        
        # We need to try all permutations of phase settings 0-4
        permutations = itertools.permutations([0, 1, 2, 3, 4])
        largest_output = 0
        
        for sequence in permutations:
            # Run the program for each amplifier - the first input being the
            # phase setting and the second being the previous amplifier's
            # output (using 0 for the first amplifier)
            output = 0
            for i in sequence:
                output = intcode.run_program(input_data, [i, output])
            
            if output > largest_output:
                largest_output = output
        
        return largest_output
    
    def _part2(self, input_data):
        
        # We need to try all permutations of phase settings 5-9
        permutations = itertools.permutations([5, 6, 7, 8, 9])
        largest_output = 0
        
        for sequence in permutations:
            amps = []
            
            # Establish the program for each amplifier and provide the first
            # input - the phase setting
            for i in sequence:
                amp = intcode.Program(input_data)
                amp.send(i)  # provide phase setting as first input
                amp.run()  # will run until further input is required
                amps.append(amp)
            
            # Continue to run each of the established amplifier programs,
            # passing them the output of the previous one in a feedback loop
            # (using 0 for the first amplifier), until the last program in the
            # chain completes
            output = 0
            while not amps[4].halt:
                for amp in amps:
                    amp.send(output)
                    amp.run()  # will run until further input is required
                    output = amp.receive()[-1]
            
            if output > largest_output:
                largest_output = output
        
        return largest_output
