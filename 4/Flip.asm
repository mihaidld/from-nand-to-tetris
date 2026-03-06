// Flips values of RAM[0] and RAM[1]
// Usage: put values in RAM[0] and RAM[1], then run this program
@R0
D=M // D = RAM[0]
@temp
M=D // temp = RAM[0]

@R1
D=M // D = RAM[1]
@R0
M=D // RAM[O] = RAM[1]

@temp
D=M // D = RAM[0]
@R1
M=D // RAM[1] = former RAM[0]

(END)
@END
0;JMP