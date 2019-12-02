import operator


def run_program(program):
    
    # Initialise memory with a copy of the intcode program
    memory = program[:]
    
    instruction_pointer = 0
    while instruction_pointer < len(program):
        opcode = memory[instruction_pointer]
        
        if opcode == 99:
            break
        elif opcode == 1:
            operation = operator.add
        elif opcode == 2:
            operation = operator.mul
        else:
            raise Exception('Unrecognised opcode')
        
        param1 = memory[instruction_pointer + 1]
        param2 = memory[instruction_pointer + 2]
        param3 = memory[instruction_pointer + 3]
        
        input1 = memory[param1]
        input2 = memory[param2]
        
        memory[param3] = operation(input1, input2)
        
        # Proceed to next instruction
        instruction_pointer += 4
    else:
        raise Exception('Reached end of program without seeing opcode 99')
    
    return memory[0]
