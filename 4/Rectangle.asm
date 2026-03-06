// Draws filled rectangle at the screen's (256 rows x 512 columns) top-left corner
// Rectangle's width is 16 pixels and height is RAM[0]
// Usage: put a non-negative number (rectangle's height) in RAM[0]

// Pseudo code
// for (i=0, i<n, i++)
// { draw 16 black pixels at beginning of row i }

// addr = SCREEN
// n = RAM[0]
// i = 0

// LOOP:
// if i > n goto END
// RAM[addr] = -1
// addr += 32 // advances to next row
// i++
// goto LOOP

// END:
// goto END


@R0
D=M
@n
M=D // n = RAM[0]

@i
M=0 // i = 0, current index which will change with loop

@SCREEN // Screen memory map 
D=A
@address
M=D // address = 16384, current address inside memory map will change with loop

(LOOP)
@i
D=M
@n
D=M-D
@END
D;JEQ // when n-i == 0 (i has reached n) we stop loop

@address
A=M
M=-1 // RAM[address] = -1, or 1111... so all 16 pixelles filled

@i
M=M+1 // i++

@32
D=A
@address
M=D+M // address += 32 (32 registers in a screen row)

@LOOP
0;JMP

(END)
@END
0;JMP