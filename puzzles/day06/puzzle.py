from ..aoc import Puzzle


class P(Puzzle):
    
    input_delimiter = None
    
    def process_input_data(self, input_data):
        
        # Map each object to the object it orbits
        orbit_map = {}
        for input_line in input_data.split('\n'):
            orbitee, orbiter = input_line.split(')')
            orbit_map[orbiter] = orbitee
        
        return orbit_map
    
    def _part1(self, input_data):
        
        # Use the orbit map to count the length of every object's hierarchy of
        # orbits to calculate the grand total number of orbits
        total_orbits = 0
        
        for orbiter, orbitee in input_data.items():
            obj_orbits = 1
            while orbitee != 'COM':
                obj_orbits += 1
                orbitee = input_data[orbitee]
            
            total_orbits += obj_orbits
        
        return total_orbits
    
    def _part2(self, input_data):
        
        # Use the orbit map to trace the YOU and SAN objects' orbital hierarchy
        # back to COM
        you_path = []
        santa_path = []
        
        for orbiter, path in (('YOU', you_path), ('SAN', santa_path)):
            while True:
                orbiter = input_data[orbiter]
                path.append(orbiter)
                if orbiter == 'COM':
                    break
        
        # Ignore all common objects in the hierarchies. The remaining objects
        # represent those for which an orbital transfer is required. Even
        # though it does not include the object at which both paths intersect
        # (since it is common to both and therefore ignored), we get the
        # correct count WITHOUT it since we are after the number of transfers
        # BETWEEN orbits, not the number of objects in the resulting path.
        transfers = set(you_path).symmetric_difference(santa_path)
        
        return len(transfers)
