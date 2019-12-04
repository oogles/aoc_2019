from collections import Counter

from ..aoc import Puzzle


def find_candidate_passwords(i, n):
    
    while True:
        digits = list(map(int, str(i)))
        matching_pair = False
        
        # Iterate over each pair of digits in the password
        for p1 in range(len(digits) - 1):
            p2 = p1 + 1
            
            # If the second of the pair is lower than the first, bring it
            # up to at least equal with it
            if digits[p2] < digits[p1]:
                digits[p2] = digits[p1]
        
        # Convert the list of digits back into a single number, by way
        # of joining the list items into a string and coercing it
        i = int(''.join(map(str, digits)))
        
        # If the resulting password is out of range, stop looking
        if i > n:
            raise StopIteration()
        
        yield digits
        
        # Increment the password by 1 so the next iteration progresses
        i += 1


class P(Puzzle):
    
    input_delimiter = ','
    
    def process_input_item(self, input_item):
        
        return int(input_item)
    
    def _part1(self, input_data):
        
        i, n = input_data
        matches = 0
        
        for candidate in find_candidate_passwords(i, n):
            if any(c >= 2 for c in Counter(candidate).values()):
                matches += 1
        
        return matches
    
    def _part2(self, input_data):
        
        i, n = input_data
        matches = 0
        
        for candidate in find_candidate_passwords(i, n):
            if any(c == 2 for c in Counter(candidate).values()):
                matches += 1
        
        return matches
