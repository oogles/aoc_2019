import importlib
import sys


def validate_day(day):
    
    day = int(day)  # could raise ValueError
    
    if day < 1 or day > 25:
        raise ValueError('Must be between 1 and 25.')
    
    return day


def get_module(day):
    
    return importlib.import_module(f'puzzles.day{day:02d}.puzzle')


def solve_puzzle(module):
    
    try:
        puzzle = module.P(sample=sample)
    except AttributeError as e:
        print(e)
        print('You should fix that.')
        sys.exit(1)
    
    puzzle.solve()

if __name__ == '__main__':
    
    # Check for "--sample" flag
    flags = sys.argv[2:]
    sample = '--sample' in flags
    
    # Extract and validate "day" argument
    try:
        day = sys.argv[1]
    except IndexError:
        print('Missing argument. Either specify 1-25 to run that day\'s puzzle, or use the --all flag to run all puzzles.')
        sys.exit(1)
    
    if day == '--all':
        # Import and execute puzzle solver for all days in the calendar
        for day in range(1, 25):
            try:
                module = get_module(day)
            except ModuleNotFoundError as e:
                # No puzzle for day, presumably no further puzzles either
                break
            
            solve_puzzle(module)
    else:
        try:
            day = validate_day(day)
        except ValueError:
            print('The "day" argument must be an integer between 1 and 25.')
            sys.exit(1)
        
        # Import and execute puzzle solver for the given day
        try:
            module = get_module(day)
        except ModuleNotFoundError as e:
            print(e)
            print(f'Have you unlocked the day {day} puzzle yet?')
            sys.exit(1)
        
        solve_puzzle(module)
