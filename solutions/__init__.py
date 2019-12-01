import datetime
import os
import sys


class AdventOfCode:
    
    day = None
    
    # Whether to process the input file line-by-line or as a whole
    process_as_list = True
    
    # The datatype of the processed input data. One of: list, str, other.
    input_type = 'list'
    
    def __init__(self, test=False):
        
        self.test = test
    
    def _get_input_file_name(self):
        
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        subdir = 'samples' if self.test else 'inputs'
        
        path = os.path.join(base_path, subdir)
        
        return '{}/day{:02d}'.format(path, self.day)
    
    def _get_input_line_data(self, input_line):
        
        return input_line
    
    def _get_input_data(self, input_data):
        
        return input_data
    
    def get_input(self):
        
        input_file = self._get_input_file_name()
        
        if self.process_as_list:
            input_data = []
            
            with open(input_file, 'r') as f:
                for line in f.readlines():
                    line = line.strip()  # trim whitespace (e.g. newlines)
                    
                    if line:
                        # Skip blank lines
                        line_data = self._get_input_line_data(line)
                        input_data.append(line_data)
        else:
            with open(input_file, 'r') as f:
                input_data = f.read().strip()  # trim whitespace (e.g. newlines)
                input_data = self._get_input_data(input_data)
        
        return input_data
    
    def _do_solve(self, solvers):
        
        print('=' * 50)
        print('')
        
        if self.test:
            print('*** USING SAMPLE INPUT ***')
            print('')
        
        print('Processing input...')
        
        start = datetime.datetime.now()
        try:
            input_data = self.get_input()
        except FileNotFoundError:
            print('No {}input data file found (looked in {}).'.format(
                'sample ' if self.test else '',
                self._get_input_file_name()
            ))
            return
        
        t = (datetime.datetime.now() - start).total_seconds()
        
        input_msg = 'Input is {} {} [{}s]'
        if self.input_type == 'list':
            print(input_msg.format(len(input_data), 'lines', t))
        if self.input_type == 'str':
            print(input_msg.format(sys.getsizeof(input_data), 'bytes', t))
        else:
            print(input_msg.format('of type', type(input_data), t))
        
        for part, solver in solvers:
            if self.input_type == 'list':
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
