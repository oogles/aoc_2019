from ..aoc import Puzzle


class P(Puzzle):
    
    input_delimiter = None
    
    width = 25
    height = 6
    
    def process_input_data(self, input_data):
        
        width = self.width
        height = self.height
        
        layers = []
        li = 0  # the index at which the current layer starts
        while li < len(input_data):
            rows = []
            ri = li  # the index at which the current row starts
            for i in range(height):
                rows.append(input_data[ri:ri + width])
                ri += width
            
            layers.append(rows)
            li += (width * height)
        
        return layers
    
    def _part1(self, input_data):
        
        min_value = None
        target_layer = None
        for layer in input_data:
            # Join all rows into a single string and count 0s
            layer_str = ''.join(layer)
            n = layer_str.count('0')
            if min_value is None or n < min_value:
                min_value = n
                target_layer = layer_str
        
        return target_layer.count('1') * target_layer.count('2')
    
    def _part2(self, input_data):
        
        width = self.width
        height = self.height
        
        # Create a template for the final image
        final_image = [['*' for i in range(width)] for j in range(height)]
        
        for y in range(height):
            for x in range(width):
                for z in range(len(input_data)):
                    pixel = input_data[z][y][x]
                    
                    # Use the pixel if it is not transparent, otherwise try the
                    # next layer
                    if pixel in ('0', '1'):
                        final_image[y][x] = pixel
                        break
                else:
                    # Uh-oh, no layer had a non-transparent pixel
                    raise Exception(f'No solid pixel found at any layer for position ({x}, {y})')
            
            # With the row completed, print it as white text on a black
            # background
            row = final_image[y]
            print(''.join(row).replace('1', '*').replace('0', ' '))
        
        return 'See output above'
