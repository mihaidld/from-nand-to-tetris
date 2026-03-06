// Pointers Array using A=M
// because M stores an address we set address register to M to select memory register at address arr
// for (i=0;i<n;i++) 
// { arr[i] = -1; }

// Suppose arr = 100 (arr variable (RAM[16]) stores address 100, n = 10

// arr = 100 array abstraction stores base address 100 in RAM
@100
D=A
@arr 
M=D //  RAM[16] = 100

// n = 10 first 10 entries to set to -1
@10
D=A
@n 
M=D // RAM[17] = 10

// initialize i = 0
@i
M=0 // RAM[18] = 0

(LOOP)
// if (i == n) goto END
@i
D=M
@n
D=D-M
@END
D;JEQ

// RAM[arr+i]= -1
@arr
D=M
@i
A=D+M // set address register to arr (100) + curent value of index i
M=-1

// i++
@i
M=M+1

@LOOP
0;JMP

(END)
@END
0;JMP

