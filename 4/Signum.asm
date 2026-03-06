// Get sign of number: if RAM[0] >= 0 then RAM[1] = 1 else RAM[1] = 0
// Usage: put a value in RAM[0], then run this program.
@R0
D=M // D = RAM[0]

@POSITIVE
D;JGE // if D >= 0 jump to POSITIVE

@R1
M=0 // RAM[1] = 0
@END
0;JMP // jump to END

(POSITIVE)
@R1
M=1 // RAM[1] = 1

(END)
@END
0;JMP // Infinite loop to end the program