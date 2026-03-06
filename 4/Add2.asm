// Program to add RAM[0] and RAM[1] and store the result in RAM[2]
// Usage: put values in RAM[0] and RAM[1], then run this program.
@0
D=M // D = RAM[0]
@1
D=D+M // D = RAM[0] + RAM[1]
@2
M=D // RAM[2] = D  
(End)
@End
0;JMP // Infinite loop to end the program 