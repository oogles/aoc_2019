from ..aoc import Puzzle


class P(Puzzle):
    
    def process_input_item(self, input_item):
        
        # This is brute force, but for each wire (each line of input), take the
        # list of directions and convert into (x, y) coordinates of every single
        # point the wire crosses
        path = []
        x = 0
        y = 0
        for direction in input_item.split(','):
            d, n = direction[0], int(direction[1:])
            for i in range(n):
                if d == 'U':
                    y += 1
                elif d == 'D':
                    y -= 1
                elif d == 'L':
                    x -= 1
                elif d == 'R':
                    x += 1
                else:
                    raise Exception('Unknown direction!')
                
                path.append((x, y))
        
        return path
    
    def _part1(self, input_data):
        
        path1, path2 = input_data
        
        # Use set intersection to find coordinates that overlap
        overlaps = set(path1).intersection(path2)
        
        # Calculate the Manhattan distance of each overlapping point from the
        # origin (0, 0), and take the minimum
        return min(abs(x) + abs(y) for x, y in overlaps)
    
    def _part2(self, input_data):
        
        path1, path2 = input_data
        
        # Use set intersection to find coordinates that overlap
        overlaps = set(path1).intersection(path2)
        
        # For each overlapping point, take the FIRST occurrence of that point
        # for EACH wire and determine the number of steps taken to reach that
        # point. Add the step values of both wires together and find the lowest
        # total. The number of steps is equal to that point's first index in
        # the wire's path, plus one (due to being 0-indexed).
        return min(path1.index(p) + path2.index(p) + 2 for p in overlaps)
