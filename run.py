import argparse
import importlib
import sys


def get_module(day):
    
    return importlib.import_module(f'puzzles.day{day:02d}.puzzle')


def solve_puzzle(module, args, v=2):
    
    try:
        puzzle = module.P(sample=args.sample, verbosity=v)
    except AttributeError as e:
        print(e)
        print('You should fix that.')
        sys.exit(1)
    
    part1 = args.part1
    part2 = args.part2
    if part1 == part2:  # either both set or neither set
        puzzle.solve()
    elif part1:
        puzzle.solve_part1()
    elif part2:
        puzzle.solve_part2()
    else:
        # https://xkcd.com/2200/
        raise Exception('How?')


def main():
    
    parser = argparse.ArgumentParser()
    
    parser.add_argument('day', nargs='?', type=int)
    parser.add_argument('--all', action='store_true')
    parser.add_argument('--sample', action='store_true')
    parser.add_argument('-p1', '--part1', action='store_true')
    parser.add_argument('-p2', '--part2', action='store_true')
    
    args = parser.parse_args()
    
    if args.all:
        # Import and execute puzzle solver for all days in the calendar
        if args.sample:
            print('\n*** USING SAMPLE DATA ***\n')
        
        print('-' * 50)
        for day in range(1, 25):
            try:
                module = get_module(day)
            except ModuleNotFoundError as e:
                # No puzzle for day, presumably no further puzzles either
                break
            
            print(f'== DAY {day} ==')
            solve_puzzle(module, args, v=1)
            print('-' * 50)
    else:
        # Import and execute puzzle solver for the given day
        day = args.day
        if not day or day < 1 or day > 25:
            print(
                'Invalid "day" argument. Either specify 1-25 to run that day\'s '
                'puzzle, or use the --all flag to run all puzzles.'
            )
            sys.exit(1)
        
        try:
            module = get_module(day)
        except ModuleNotFoundError as e:
            print(e)
            print(f'Has a solution been written for the day {day} puzzle yet?')
            sys.exit(1)
        
        solve_puzzle(module, args, v=2)

if __name__ == '__main__':
    main()
