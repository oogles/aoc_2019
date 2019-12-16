import math
from collections import defaultdict

from ..aoc import Puzzle


class P(Puzzle):
    
    input_delimiter = None
    
    def process_input_data(self, input_data):
        
        reactions = {}
        
        for row in input_data.split('\n'):
            input_str, output_str = row.split(' => ')
            
            quantity, material = output_str.split(' ')
            
            inputs = []
            for i in input_str.split(', '):
                qty, mat  = i.split(' ')
                inputs.append((mat, int(qty)))
            
            reactions[material] = {
                'quantity': int(quantity),
                'inputs': inputs
            }
        
        return reactions
    
    def run_reaction(self, material, quantity, reactions, leftovers):
        
        data = reactions[material]
        output_quantity = data['quantity']
        ore_required = 0
        
        # Determine the number of reactions required to produce the desired
        # quantity by first subtracting any already available and then dividing
        # by the quantity produced by a single reaction
        available_quantity = min(leftovers[material], quantity)
        num_reactions = math.ceil((quantity - available_quantity) / output_quantity)
        
        for input_material, input_quantity in data['inputs']:
            input_quantity *= num_reactions
            
            if input_material == 'ORE':
                ore_required += input_quantity
            else:
                ore_required += self.run_reaction(input_material, input_quantity, reactions, leftovers)
        
        # Store any quantity created by the reaction that exceeds the required
        # amount. This also has the effect of subtracting any leftovers from
        # earlier reactions, as the amount produced will be LESS than required.
        leftovers[material] += (output_quantity * num_reactions) - quantity
        
        return ore_required
    
    def _part1(self, input_data):
        
        leftovers = defaultdict(lambda: 0)
        return self.run_reaction('FUEL', 1, input_data, leftovers)
    
    def _part2(self, input_data):
        
        leftovers = defaultdict(lambda: 0)
        ore_remaining = 1000000000000
        fuel_total = 0
        
        # For performance reasons, run reactions with quantities of
        # ever-decreasing orders of magnitude, from 1 million down to 1
        reaction_amount = 1000000
        
        while reaction_amount >= 1:
            while True:
                # Create a copy of the leftovers dictionary before each attempt,
                # so that it can be reset if the attempt proves to use too much
                # ore
                leftovers_copy = leftovers.copy()
                ore_used = self.run_reaction('FUEL', reaction_amount, input_data, leftovers_copy)
                
                if ore_used > ore_remaining:
                    break
                
                ore_remaining -= ore_used
                fuel_total += reaction_amount
                leftovers = leftovers_copy
            
            reaction_amount //= 10
        
        return fuel_total
