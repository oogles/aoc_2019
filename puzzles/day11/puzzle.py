from ..aoc import Puzzle
from ..intcode import Program


class P(Puzzle):
    
    input_delimiter = ','
    
    def process_input_item(self, input_item):
        
        return int(input_item)
    
    def paint(self, program, initial_colour):
        
        # Map grid positions to their colours. The robot starts at (0, 0),
        # facing up. Directions are: 0 - up, 1 - right, 2 - down, 3 - left.
        grid = {
            (0, 0): initial_colour
        }
        current_position = (0, 0)
        current_direction = 0
        direction_delta = {
            0: (0, 1),  # facing up, increase y
            1: (1, 0),  # facing right, increase x
            2: (0, -1),  # facing down, decrease y
            3: (-1, 0),  # facing left, decrease x
        }
        
        robot = Program(program)
        
        while not robot.halt:
            # Input the colour of the square at the current position and run
            # until further input is required or the program completes. Panels
            # in the grid are black (0) by default.
            robot.send(grid.get(current_position, 0))
            robot.run()
            
            output_array = robot.receive()
            colour, direction = output_array
            
            # Update panel colour
            grid[current_position] = colour
            
            # The current direction becomes +1 if turning right, -1 if turning
            # left, modulo 4 to keep it within the bounds of 0-3
            current_direction = (current_direction + 1 if direction else current_direction - 1) % 4
            
            # The current position moves by one in the direction the robot is
            # now facing, as dictated by the configured direction deltas
            current_x, current_y = current_position
            delta_x, delta_y = direction_delta[current_direction]
            current_position = (current_x + delta_x, current_y + delta_y)
        
        return grid
    
    def _part1(self, input_data):
        
        grid = self.paint(input_data, 0)
        
        return len(grid)  # number of panels painted at least once
    
    def _part2(self, input_data):
        
        grid = self.paint(input_data, 1)
        
        # Get the width and height of the painted area
        min_x = min(grid.keys(), key=lambda i: i[0])[0]
        max_x = max(grid.keys(), key=lambda i: i[0])[0]
        min_y = min(grid.keys(), key=lambda i: i[1])[1]
        max_y = max(grid.keys(), key=lambda i: i[1])[1]
        
        # Draw the result, assuming unpainted panels are black. Iterate high to
        # low (top to bottom) for the y-direction and low to high (left to
        # right) for the x-direction.
        output = ['\n']
        for y in range(max_y, min_y - 1, -1):
            for x in range(min_x, max_x + 1):
                colour = grid.get((x, y), 0)
                output.append('#' if colour else ' ')
            
            output.append('\n')
        
        return ''.join(output)
