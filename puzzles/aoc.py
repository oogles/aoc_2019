import datetime
import inspect
import os
import sys


class Puzzle:
    
    # The delimiter to use to separate the input data into a list for subsequent
    # processing. E.g. '\n', ',', etc. Delimited items can be processed prior to
    # being added to the input list by overriding _process_input_item().
    # Set to None to read the data in whole. In this case, data can be processed
    # by overriding _process_input_data().
    input_delimiter = '\n'
    
    def __init__(self, sample=False):
        
        self.sample = sample
    
    def get_input_file_name(self):
        
        path = os.path.dirname(os.path.abspath(inspect.getfile(self.__class__)))
        filename = 'sample' if self.sample else 'input'
        
        return os.path.join(path, filename)
    
    def process_input_item(self, input_line):
        
        return input_line
    
    def process_input_data(self, input_data):
        
        return input_data
    
    def get_input(self):
        
        input_file = self.get_input_file_name()
        delimiter = self.input_delimiter
        process_item = self.process_input_item
        
        with open(input_file, 'r') as f:
            if delimiter == '\n':
                # Trim whitespace from and process each line in the input file,
                # skipping any blank lines
                input_data = []
                
                for line in f.readlines():
                    line = line.strip()
                    if line:
                        input_data.append(process_item(line))
            else:
                raw_input = f.read().strip()  # trim whitespace (e.g. newlines)
                
                if delimiter:
                    # Trim whitespace from and process each item in the raw
                    # input data after applying the configured delimiter
                    input_data = [process_item(item.strip()) for item in raw_input.split(delimiter)]
                else:
                    # Process the raw input data directly
                    input_data = self.process_input_data(raw_input)
        
        return input_data
    
    def _do_solve(self, solvers):
        
        print('=' * 50)
        print('')
        
        if self.sample:
            print('*** USING SAMPLE INPUT ***')
            print('')
        
        print('Processing input...')
        
        start = datetime.datetime.now()
        try:
            input_data = self.get_input()
        except FileNotFoundError:
            print('No {}input data file found (looked in {}).'.format(
                'sample ' if self.sample else '',
                self.get_input_file_name()
            ))
            return
        
        t = (datetime.datetime.now() - start).total_seconds()
        
        if self.input_delimiter == '\n':
            input_desc = f'has {len(input_data)} lines'
        elif self.input_delimiter:
            input_desc = f'has {len(input_data)} items'
        else:
            size = sys.getsizeof(input_data)
            input_desc = f'is {size} bytes'
        
        print(f'Input {input_desc} ({type(input_data)}) [{t}s]')
        
        for part, solver in solvers:
            if self.input_delimiter:
                # Copy the data so each part is free to manipulate it without
                # affecting subsequent parts
                part_input_data = input_data[:]
            else:
                part_input_data = input_data
            
            print('')
            print('Solving Part {}...'.format(part))
            
            start = datetime.datetime.now()
            solution = solver(part_input_data)
            t = (datetime.datetime.now() - start).total_seconds()
            
            print('Solution: {} [{}s]'.format(solution, t))
        
        print('')
        print('=' * 50)
    
    def _part1(self, input_data):
        
        raise NotImplementedError()
    
    def _part2(self, input_data):
        
        raise NotImplementedError()
    
    def solve_part1(self):
        
        self._do_solve([(1, self._part1)])
    
    def solve_part2(self):
        
        self._do_solve([(2, self._part2)])
    
    def solve(self):
        
        self._do_solve([(1, self._part1), (2, self._part2)])
