// Computes R2 = R0 * R1
// Usage : R0 >= 0, R1 >= 0 and R0*R1<32678 (< 2^15)

// Pseudo code
// n1 = R0
// n2 = R1
// mult = 0
// i = 0

// LOOP:
// if i = n2 goto STOP
// mult += n1
// i++
// goto LOOP

// STOP:
// R2 = mult

@R0
D=M
@n1
M=D // n1 = R0
@R1
D=M
@n2
M=D // n2 = R1
@i
M=0 // i = 0
@mult
M=0 // mult = 0

(LOOP)
@i
D=M // D = current i
@n2
D=M-D // D = n2 - i
@STOP
D;JEQ // if i = n2 goto STOP
@n1
D=M
@mult
M=D+M // mult += n1
@i
M=M+1 // i++
@LOOP
0;JMP

(STOP)
@mult
D=M // D = mult
@R2
M=D // R2 = mult

(END)
@END
0;JMP