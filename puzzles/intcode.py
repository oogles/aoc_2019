from collections import defaultdict


class UNSET:
    pass


class AwaitInput(Exception):
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
    
    def get_input_params(self, state, memory):
        
        ptr = self.ptr
        param_modes = self.param_modes
        
        inputs = []
        for i in range(1, self.num_input_params + 1):
            value = memory[ptr + i]
            
            try:
                mode = param_modes[-i]
            except IndexError:
                mode = '0'
            
            if mode in ['0', '2']:
                if mode == '0':
                    # Positional mode - the value is an absolute memory address
                    addr = value
                else:
                    # Relative mode - the value is a relative memory address
                    addr = state['relative_base'] + value
                
                # A memory address cannot be negative
                if addr < 0:
                    raise Exception(f'Negative memory address ({addr})!')
                
                # Retrieve the real value from the specified memory address
                value = memory[addr]
            
            inputs.append(value)
        
        return inputs
    
    def get_output_param(self, state, memory):
        
        if not self.has_output_param:
            return None
        
        ptr = self.ptr + self.length - 1
        value = memory[ptr]
        
        try:
            # The output param mode is the left-most mode value
            mode = self.param_modes[-(self.num_input_params + 1)]
        except IndexError:
            mode = '0'
        
        if mode == '1':
            raise Exception('Output parameters can never be in immediate mode.')
        elif mode == '2':
            # Relative mode - the value is a relative memory address
            value += state['relative_base']
        
        # A memory address cannot be negative
        if value < 0:
            raise Exception(f'Negative output address ({value})!')
        
        return value
    
    def execute(self, state, *inputs):
        
        raise NotImplementedError()
    
    def get_next_instruction_pointer(self):
        
        return self.ptr + self.length


class AddInstruction(Instruction):
    
    num_input_params = 2
    has_output_param = True
    
    def execute(self, state, a, b):
        
        return a + b


class MultiplyInstruction(Instruction):
    
    num_input_params = 2
    has_output_param = True
    
    def execute(self, state, a, b):
        
        return a * b


class InputInstruction(Instruction):
    
    num_input_params = 0
    has_output_param = True
    
    def execute(self, state, value=None):
        
        if value is None:
            raise AwaitInput()
        
        return value


class OutputInstruction(Instruction):
    
    num_input_params = 1
    has_output_param = False
    
    def execute(self, state, value):
        
        print(value)
        
        # Does not return a result, instead it updates the overall program's
        # internal state
        state['output'] = value


class JumpInstruction(Instruction):
    
    num_input_params = 2
    has_output_param = False
    
    def __init__(self, *args, **kwargs):
        
        super().__init__(*args, **kwargs)
        
        self.jump_to = UNSET
    
    def get_next_instruction_pointer(self):
        
        if self.jump_to is UNSET:
            raise Exception('Instruction not executed.')
        elif self.jump_to is not None:
            # Jumping - the next instruction pointer is the jump value
            return self.jump_to
        else:
            # Not jumping - proceed to the next instruction as per usual
            return super().get_next_instruction_pointer()


class JumpIfTrueInstruction(JumpInstruction):
    
    def execute(self, state, test_param, jump_param):
        
        if test_param > 0:
            self.jump_to = jump_param
        else:
            self.jump_to = None


class JumpIfFalseInstruction(JumpInstruction):
    
    def execute(self, state, test_param, jump_param):
        
        if test_param == 0:
            self.jump_to = jump_param
        else:
            self.jump_to = None


class LessThanInstruction(Instruction):
    
    num_input_params = 2
    has_output_param = True
    
    def execute(self, state, a, b):
        
        if a < b:
            return 1
        
        return 0


class EqualsInstruction(Instruction):
    
    num_input_params = 2
    has_output_param = True
    
    def execute(self, state, a, b):
        
        if a == b:
            return 1
        
        return 0


class RelativeBaseOffsetInstruction(Instruction):
    
    num_input_params = 1
    has_output_param = False
    
    def execute(self, state, value):
        
        # Does not return a result, instead it updates the overall program's
        # internal state
        state['relative_base'] += value


class Program:
    
    def __init__(self, intcodes):
        
        self._length = len(intcodes)
        
        self._manual_input = None
        
        self.instruction_pointer = 0
        self.halt = False
        self.awaiting_input = False
        
        # Initialise the internal state of the program, as accessible/modifiable
        # by instructions
        self.state = {
            'output': None,
            'relative_base': 0
        }
        
        # Initialise memory with the intcode program. Use a defaultdict to make
        # addresses beyond the length of the original program accessible - and
        # consider any such addresses to contain 0 by default.
        self.memory = defaultdict(lambda: 0, {i: v for i, v in enumerate(intcodes)})
    
    def get_instruction(self, ptr):
        
        instruction_descriptor = str(self.memory[ptr])
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
            9: RelativeBaseOffsetInstruction,
        }
        
        try:
            instruction = opcode_map[opcode]
        except KeyError:
            raise KeyError(f'Unrecognised opcode ({opcode}).')
        
        return instruction(ptr, param_modes)
    
    def run(self):
        
        ptr = self.instruction_pointer
        state = self.state
        
        while ptr < self._length:
            try:
                instruction = self.get_instruction(ptr)
            except StopIteration:
                # Successfully reached the end of the program, enter "halt"
                # state
                self.halt = True
                break
            
            # Use inputs to execute the instruction and generate a result.
            # Specific "input" instructions require manual input entry - the
            # value is not read from memory. If such a value has already been
            # provided (via set_input()), use it. Otherwise, read inputs as
            # per usual.
            if self._manual_input is not None:
                inputs = [self._manual_input]
                self._manual_input = None  # clear manual input value once used
            else:
                inputs = instruction.get_input_params(state, self.memory)
            
            try:
                result = instruction.execute(state, *inputs)
            except AwaitInput:
                # Pause the program to await manual input via set_input()
                self.awaiting_input = True
                return state['output']  # return interstitial output
            
            output_param = instruction.get_output_param(state, self.memory)
            if output_param is not None:
                self.memory[output_param] = result
            
            # Proceed to next instruction
            ptr = self.instruction_pointer = instruction.get_next_instruction_pointer()
        else:
            raise Exception('Reached end of program without seeing opcode 99')
        
        # Return potentially-interstitial output - get_output() should be used
        # for retrieving final output
        return state['output']
    
    def set_input(self, value):
        
        try:
            value = int(value)
        except ValueError:
            print('Invalid input. Must be an integer.')
            return
        
        self._manual_input = value
        self.awaiting_input = False
    
    def get_output(self):
        
        if not self.halt:
            raise Exception('Program was not successfully terminated')
        
        # Return explicitly-generated output if there is any, otherwise return
        # the value in memory address 0
        output = self.state['output']
        if output is not None:
            return output
        else:
            return self.memory[0]


def run_program(program, manual_inputs=None):
    
    program = Program(program)
    
    while not program.halt:
        program.run()
        
        while program.awaiting_input:
            if manual_inputs:
                value = manual_inputs.pop(0)
            else:
                value = input('Input: ')
            
            program.set_input(value)
    
    return program.get_output()
