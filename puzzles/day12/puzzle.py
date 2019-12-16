from copy import deepcopy
from fractions import gcd
from functools import reduce
from itertools import combinations

from ..aoc import Puzzle


class P(Puzzle):
    
    def process_input_item(self, input_item):
        
        position = [int(v.split('=')[1]) for v in input_item.strip('<>').split(',')]
        
        # Make each item a combination of the position extracted above and a
        # three-dimensional velocity with initial values of of 0
        return (position, [0, 0, 0])
    
    def step(self, moons, moon_pairs):
        
        # Apply gravity by comparing the positions of each pair of moons
        for m1, m2 in moon_pairs:
            m1_pos, m1_vel = m1
            m2_pos, m2_vel = m2
            
            for j in range(3):
                m1_coord = m1_pos[j]
                m2_coord = m2_pos[j]
                
                if m1_coord > m2_coord:
                    m1_vel[j] -= 1
                    m2_vel[j] += 1
                elif m2_coord > m1_coord:
                    m1_vel[j] += 1
                    m2_vel[j] -= 1
        
        # Update positions
        for position, velocity in moons:
            for i in range(3):
                position[i] += velocity[i]
    
    def _part1(self, input_data):
        
        moons = deepcopy(input_data)  # deepcopy due to nested lists
        steps = 0
        
        if self.sample:
            max_steps = 10
        else:
            max_steps = 1000
        
        moon_pairs = list(combinations(moons, 2))
        while steps < max_steps:
            self.step(moons, moon_pairs)
            steps += 1
        
        total_energy = 0
        for position, velocity in moons:
            potential_energy = sum(abs(v) for v in position)
            kinetic_energy = sum(abs(v) for v in velocity)
            total_energy += potential_energy * kinetic_energy
        
        return total_energy
    
    def _part2(self, input_data):
        
        pass
