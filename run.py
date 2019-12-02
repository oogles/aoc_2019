import importlib
import sys


if __name__ == '__main__':
    # Extract and validate "day" argument
    try:
        day = int(sys.argv[1])
    except IndexError:
        print('Missing "day" argument.')
        sys.exit(1)
    except ValueError:
        day = -1
    
    if day < 1 or day > 25:
        print('The "day" argument must be an integer between 1 and 25.')
        sys.exit(1)
    
    # Extract and validate "sample" argument
    sample = False
    
    # Import and execute puzzle solver
    try:
        module = importlib.import_module(f'puzzles.day{day:02d}.puzzle')
    except ModuleNotFoundError as e:
        print(e)
        print(f'Have you unlocked the day {day} puzzle yet?')
        sys.exit(1)
    
    try:
        puzzle = module.P(sample=sample)
    except AttributeError as e:
        print(e)
        print('You should fix that.')
        sys.exit(1)
    
    puzzle.solve()
