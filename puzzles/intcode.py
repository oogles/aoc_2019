class UNSET:
    pass


class Instruction:
    
    num_input_params = 0
    has_output_param = False
    
    def __init__(self, ptr, param_modes):
        
        self.ptr = ptr
        self.param_modes = param_modes
        
        # The instruction's length covers its first value (containing the
        # opcode), a variable number of input parameters, and the optional
        # output parameter
        self.length = 1 + self.num_input_params + (1 if self.has_output_param else 0)
    
    def get_input_params(self, memory):
        
        ptr = self.ptr
        param_modes = self.param_modes
        
        inputs = []
        for i in range(1, self.num_input_params + 1):
            value = memory[ptr + i]
            
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
        
        return inputs
    
    def get_output_param(self):
        
        if not self.has_output_param:
            return None
        
        return self.ptr + self.length - 1
    
    def execute(self, *inputs):
        
        raise NotImplementedError()
    
    def get_next_instruction_pointer(self):
        
        return self.ptr + self.length


class AddInstruction(Instruction):
    
    num_input_params = 2
    has_output_param = True
    
    def execute(self, a, b):
        
        return a + b


class MultiplyInstruction(Instruction):
    
    num_input_params = 2
    has_output_param = True
    
    def execute(self, a, b):
        
        return a * b


class InputInstruction(Instruction):
    
    num_input_params = 0
    has_output_param = True
    
    def execute(self):
        
        while True:
            value = input('Input: ')
            
            try:
                value = int(value)
                break
            except ValueError:
                print('Invalid input. Must be an integer.')
                continue
        
        return value


class OutputInstruction(Instruction):
    
    num_input_params = 1
    has_output_param = False
    
    def execute(self, value):
        
        print(value)


class JumpInstruction(Instruction):
    
    num_input_params = 2
    has_output_param = False
    
    def __init__(self, *args, **kwargs):
        
        super().__init__(*args, **kwargs)
        
        self.jump_to = UNSET
    
    def get_next_instruction_pointer(self):
        
        if self.jump_to is UNSET:
            raise Exception('Instruction not executed.')
        elif self.jump_to:
            # Jumping - the next instruction pointer is the jump value
            return self.jump_to
        else:
            # Not jumping - proceed to the next instruction as per usual
            return super().get_next_instruction_pointer()


class JumpIfTrueInstruction(JumpInstruction):
    
    def execute(self, test_param, jump_param):
        
        if test_param > 0:
            self.jump_to = jump_param
        else:
            self.jump_to = None


class JumpIfFalseInstruction(JumpInstruction):
    
    def execute(self, test_param, jump_param):
        
        if test_param == 0:
            self.jump_to = jump_param
        else:
            self.jump_to = None


class LessThanInstruction(Instruction):
    
    num_input_params = 2
    has_output_param = True
    
    def execute(self, a, b):
        
        if a < b:
            return 1
        
        return 0


class EqualsInstruction(Instruction):
    
    num_input_params = 2
    has_output_param = True
    
    def execute(self, a, b):
        
        if a == b:
            return 1
        
        return 0


def get_instruction(ptr, memory):
    
    instruction_descriptor = str(memory[ptr])
    opcode = int(instruction_descriptor[-2:])
    param_modes = instruction_descriptor[:-2]
    
    if opcode == 99:
        raise StopIteration()
    
    opcode_map = {
        1: AddInstruction,
        2: MultiplyInstruction,
        3: InputInstruction,
        4: OutputInstruction,
        5: JumpIfTrueInstruction,
        6: JumpIfFalseInstruction,
        7: LessThanInstruction,
        8: EqualsInstruction,
    }
    
    try:
        instruction = opcode_map[opcode]
    except KeyError:
        raise KeyError(f'Unrecognised opcode ({opcode}).')
    
    return instruction(ptr, param_modes)


def run_program(program):
    
    # Initialise memory with a copy of the intcode program
    memory = program[:]
    
    instruction_pointer = 0
    while instruction_pointer < len(program):
        
        try:
            instruction = get_instruction(instruction_pointer, memory)
        except StopIteration:
            break
        
        # Use inputs to execute the instruction and generate a result
        inputs = instruction.get_input_params(memory)
        result = instruction.execute(*inputs)
        
        # Write output to memory, if necessary
        output_param = instruction.get_output_param()
        if output_param is not None:
            output_pointer = memory[output_param]
            memory[output_pointer] = result
        
        # Proceed to next instruction
        instruction_pointer = instruction.get_next_instruction_pointer()
    else:
        raise Exception('Reached end of program without seeing opcode 99')
    
    return memory[0]
