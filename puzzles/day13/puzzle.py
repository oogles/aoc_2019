from ..aoc import Puzzle
from ..intcode import Program


class P(Puzzle):
    
    input_delimiter = ','
    
    def process_input_item(self, input_item):
        
        return int(input_item)
    
    def _part1(self, input_data):
        
        # Map grid positions to the objects drawn in those positions
        grid = {}
        
        game = Program(input_data)
        game.run()
        output = game.receive()
        
        i = 0
        while i < len(output):
            x, y, obj = output[i:i + 3]
            grid[(x, y)] = obj
            i += 3
        
        block_tile = 2
        
        return len(list(filter(lambda v: v == block_tile, grid.values())))
    
    def _part2(self, input_data):
        
        grid = {}  # map grid positions to the objects drawn in those positions
        sprites = {
            0: ' ',  # empty tile
            1: '|',  #
            2: '#',  #
            3: '=',  #
            4: '*',  # ball
        }
        score = 0
        
        input_data[0] = 2  # insert 2 quarters
        
        game = Program(input_data)
        
        while not game.halt:
            game.run()
            output = game.receive()
            
            i = 0
            while i < len(output):
                x, y, obj = output[i:i + 3]
                
                if x == -1 and y == 0:
                    score = obj
                else:
                    grid[(x, y)] = obj
                
                i += 3
            
            # Draw the screen (if you want to watch)
            # max_x = max([x for x, y in grid.keys()])
            # max_y = max([y for x, y in grid.keys()])
            #
            # for y in range(max_y + 1):
            #     for x in range(max_x + 1):
            #         obj = grid[(x, y)]
            #         print(sprites[obj], end='')
            #
            #     print()  # newline
            #
            # print(f'Score: {score}')
            
            # Find the ball and paddle tiles
            ball_obj = 4
            ball_x = 0
            paddle_obj = 3
            paddle_x = 0
            for coord, obj in grid.items():
                if obj == ball_obj:
                    ball_x = coord[0]
                elif obj == paddle_obj:
                    paddle_x = coord[0]
            
            # Move the paddle to align with the ball
            if paddle_x == ball_x:
                game.send(0)  # don't move
            elif paddle_x < ball_x:
                game.send(1)  # move right
            else:
                game.send(-1)  # move left
        
        return score
