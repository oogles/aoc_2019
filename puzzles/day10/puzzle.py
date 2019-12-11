from collections import defaultdict
from decimal import Decimal

from ..aoc import Puzzle


class P(Puzzle):
    
    input_delimiter = None
    
    def process_input_data(self, input_data):
        
        coordinates = []
        for y, line in enumerate(input_data.split('\n')):
            for x, obj in enumerate(line):
                if obj == '#':
                    coordinates.append((x, y))
        
        return coordinates
    
    def process_asteroids(self, asteroids, x1, y1):
        
        grouped = defaultdict(list)
        
        for x2, y2 in asteroids:
            # Find the slope of the line formed between the two positions - no
            # two asteroids with the same slope will be visible. Need to
            # consider the "quadrant" of the slope - asteroids on vertical or
            # horizontal slopes in different directions are still visible.
            # Quadrants also help processing asteroids in order in part 2.
            # Quadrants are: 0 - top left, 1 - bottom left, 2 - bottom right,
            # and 3 - top right.
            if x2 == x1 and y2 == y1:
                continue  # same point, ignore
            elif x2 >= x1 and y2 < y1:
                quadrant = 0
            elif x2 > x1 and y2 >= y1:
                quadrant = 1
            elif x2 <= x1 and y2 > y1:
                quadrant = 2
            elif x2 < x1 and y2 <= y1:
                quadrant = 3
            else:
                # https://xkcd.com/2200/
                raise Exception('How?')
            
            if x2 == x1:
                # The slope equation doesn't work for vertical lines, use 0.
                # While this is technically the same as a horizontal slope,
                # coupling it with the quadrant disambiguates it, and a value
                # of 0 allows vertical slopes to be ordered ahead of others for
                # part 2.
                m = 0
            else:
                m = (y2 - y1) / (x2 - x1)
            
            key = (quadrant, m)
            grouped[key].append((x2, y2))
        
        return grouped
    
    def _part1(self, input_data):
        
        best_position = None
        max_visible = 0
        
        for x, y in input_data:
            total_visible = len(self.process_asteroids(input_data, x, y))
            
            if total_visible > max_visible:
                max_visible = total_visible
                best_position = (x, y)
        
        print('Best:', best_position)
        return max_visible
    
    def _part2(self, input_data):
        
        if self.sample:
            laser_x = 5
            laser_y = 8
        else:
            laser_x = 22
            laser_y = 19
        
        # Process the asteroids into their quadrant/slope groups. Sort the
        # asteroids under each group by their distance from the laser, so that
        # each sweep targets the *visible* asteroid in that group.
        asteroids = self.process_asteroids(input_data, laser_x, laser_y)
        for roids in asteroids.values():
            roids.sort(key=lambda coord: abs(coord[0] - laser_x) + abs(coord[1] - laser_y))
        
        bet_target = 200
        bet_target_coord = None
        
        i = 0
        while not bet_target_coord and asteroids:
            # Loop asteroid groups in order of a clockwise sweep (using the
            # fact that they are keyed by the combined quadrant/slope). Pop the
            # nearest asteroid in each group from the list as it gets vaporised
            # by the laser.
            for key in sorted(asteroids.keys()):
                roids = asteroids[key]
                try:
                    vaporised_coord = roids.pop(0)
                except IndexError:
                    # No more asteroids in group, remove the group
                    del asteroids[key]
                    continue
                
                i += 1
                if i == bet_target:
                    bet_target_coord = vaporised_coord
                    break
        
        print('200th:', bet_target_coord)
        if bet_target_coord:
            return bet_target_coord[0] * 100 + bet_target_coord[1]
        else:
            return None
