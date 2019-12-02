from ..aoc import Puzzle


class P(Puzzle):
    
    def process_input_item(self, input_item):
        
        return int(input_item)
    
    def _part1(self, input_data):
        
        return sum([(m // 3) - 2 for m in input_data])
    
    def _part2(self, input_data):
        
        total_fuel = 0
        
        for mass in input_data:
            module_fuel = 0
            while mass > 0:
                fuel = max((mass // 3) - 2, 0)
                module_fuel += fuel
                mass = fuel
            
            total_fuel += module_fuel
        
        return total_fuel
