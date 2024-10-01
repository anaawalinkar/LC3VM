
#memory for LC-3 VM 
#(65,536 locations, 16-bit words)
MEMORY_SIZE = 65536
memory = [0] * MEMORY_SIZE

#LC-3 registers
registers = [0] * 8

#special registers
PC = 0
COND = 0

# Opcodes
OP_ADD = 0b0001
OP_AND = 0b0101
OP_BR = 0b0000

PC = 0x3000  #set starting program counter

# main loop for VM
def run_vm():
    global running
    global PC
    running = True
    while running:
        instr = memory[PC]
        PC += 1

        #decode opcode
        opcode = instr >> 12

        if opcode == OP_ADD:
           execute_add(instr)
        elif opcode == OP_AND:
            execute_and(instr)
        elif opcode == OP_BR:
            execute_br(instr)
        elif (instr & 0xF000) == 0xF000:  
            execute_trap(instr)
        else:
            running = False  


#condition flags
FL_POS = 1 
FL_ZRO = 2  
FL_NEG = 4  

def update_flags(r):
    global COND
    if registers[r] == 0:
        COND = FL_ZRO
    elif registers[r] >> 15: 
        COND = FL_NEG
    else:
        COND = FL_POS

#ADD instruction
def execute_add(instr):
    #destination register
    r0 = (instr >> 9) & 0x7
    #firstsource register
    r1 = (instr >> 6) & 0x7
    #immediate mode
    imm_flag = (instr >> 5) & 0x1

    if imm_flag:
        imm5 = sign_extend(instr & 0x1F, 5)
        registers[r0] = registers[r1] + imm5
    else:
        r2 = instr & 0x7
        registers[r0] = registers[r1] + registers[r2]

    update_flags(r0)

#AND instruction
def execute_and(instr):
    #destination register
    r0 = (instr >> 9) & 0x7
    #firstsource register
    r1 = (instr >> 6) & 0x7
    # immediate mode
    imm_flag = (instr >> 5) & 0x1

    if imm_flag:
        imm5 = sign_extend(instr & 0x1F, 5)
        registers[r0] = registers[r1] & imm5
    else:
        r2 = instr & 0x7
        registers[r0] = registers[r1] & registers[r2]

    update_flags(r0)

#helper function
def sign_extend(x, bit_count):
    if (x >> (bit_count - 1)) & 1:
        x |= (0xFFFF << bit_count)
    return x

def execute_br(instr):
    pc_offset = sign_extend(instr & 0x1FF, 9)
    cond_flag = (instr >> 9) & 0x7
    if cond_flag & COND:
        global PC
        PC += pc_offset

def execute_ld(instr):
    r0 = (instr >> 9) & 0x7
    pc_offset = sign_extend(instr & 0x1FF, 9)
    registers[r0] = memory[PC + pc_offset]
    update_flags(r0)

def execute_ldr(instr):
    r0 = (instr >> 9) & 0x7
    base_r = (instr >> 6) & 0x7
    offset = sign_extend(instr & 0x3F, 6)
    registers[r0] = memory[registers[base_r] + offset]
    update_flags(r0)

def execute_lea(instr):
    r0 = (instr >> 9) & 0x7
    pc_offset = sign_extend(instr & 0x1FF, 9)
    registers[r0] = PC + pc_offset
    update_flags(r0)

def trap_getc():
    # trap routine, read single character from input
    registers[0] = ord(input()[0])

def trap_out():
    # trap routine, output character in R0 to console
    print(chr(registers[0]), end='')

def trap_halt():
    print("Halt")
    global running
    running = False

# trap vector table
TRAP_GETC = 0x20
TRAP_OUT = 0x21
TRAP_HALT = 0x25

def execute_trap(instr):
    trap_vector = instr & 0xFF
    if trap_vector == TRAP_GETC:
        trap_getc()
    elif trap_vector == TRAP_OUT:
        trap_out()
    elif trap_vector == TRAP_HALT:
        trap_halt()


def run_vm():
    global PC
    running = True
    while running:
        # fetch instruction
        instr = memory[PC] 
        PC += 1

        # Debugging print
        print(f"PC: {PC}, Instruction: {hex(instr)}, Registers: {registers}, Flags: {COND}")

        opcode = instr >> 12

memory[0x3000] = 0xF021  # trap out
registers[0] = ord('A')  # set Register0 to ascii value of 'A'

run_vm() 

