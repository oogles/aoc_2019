import operator


def _input():
    
    while True:
        value = input('Input: ')
        
        try:
            value = int(value)
            break
        except ValueError:
            print('Invalid input. Must be an integer.')
            continue
    
    return value


def _output(value):
    
    print(value)


def run_program(program):
    
    # Initialise memory with a copy of the intcode program
    memory = program[:]
    
    instruction_pointer = 0
    while instruction_pointer < len(program):
        
        instruction_descriptor = str(memory[instruction_pointer])
        opcode = int(instruction_descriptor[-2:])
        param_modes = instruction_descriptor[:-2]
        
        if opcode == 99:
            break
        elif opcode == 1:
            operation = operator.add
            num_input_params = 2
            has_output_param = True
        elif opcode == 2:
            operation = operator.mul
            num_input_params = 2
            has_output_param = True
        elif opcode == 3:
            operation = _input
            num_input_params = 0
            has_output_param = True
        elif opcode == 4:
            operation = _output
            num_input_params = 1
            has_output_param = False
        else:
            raise Exception(f'Unrecognised opcode ({opcode}).')
        
        inputs = []
        for i in range(1, num_input_params + 1):
            value = memory[instruction_pointer + i]
            
            try:
                mode = param_modes[-i]
            except IndexError:
                mode = '0'
            
            if mode == '0':
                # Positional mode, retrieve the real value from the specified
                # memory address. A memory address cannot be negative.
                if value < 0:
                    raise Exception(f'Negative memory address ({value})!')
                
                value = memory[value]
            
            inputs.append(value)
        
        result = operation(*inputs)
        
        if has_output_param:
            output_pointer = memory[instruction_pointer + num_input_params + 1]
            memory[output_pointer] = result
        
        # Proceed to next instruction, skipping over the instruction descriptor
        # and the appropriate number of parameters
        instruction_pointer += (1 + num_input_params + (1 if has_output_param else 0))
    else:
        raise Exception('Reached end of program without seeing opcode 99')
    
    return memory[0]
