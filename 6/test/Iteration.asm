// Computes RAM[1] = 1 + 2 + ... + RAM[0]
// Usage: RAM[0] stores strictly positive int

// Pseudo code
// n = R0
// i = 1
// sum = 0

// LOOP:
// if i > n goto STOP
// sum += i
// i++
// goto LOOP

// STOP:
// R1 = sum

@R0
D = M
@n
M=D// n = R0
@i
M=1 // i = 1
@sum
M=0 // sum = 0

(LOOP)
    @i
    D=M // D = current i
    @n
    D=M-D // D = n - i
    @STOP
    D;JLT // if n-i < 0 (i > n) goto STOP
    @i
    D=M // D = i
    @sum
    M=D+M // sum += i
    @i
    M=M+1 // i++
    @LOOP
    0;JMP

(STOP)
    @sum
    D=M // D = sum
    @R1
    M=D // R1 = sum

(END)
    @END
    0;JMP