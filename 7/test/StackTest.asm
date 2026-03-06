
// push constant 17
@17
D=A
@SP
AM=M+1
A=A-1
M=D

// push constant 17
@17
D=A
@SP
AM=M+1
A=A-1
M=D

// eq
@SP
AM=M-1
D=M
A=A-1
D=M-D
@TRUE0
D;JEQ
@SP
A=M-1
M=0
@STOP0
0;JMP
(TRUE0)
@SP
A=M-1
M=-1
(STOP0)

// push constant 17
@17
D=A
@SP
AM=M+1
A=A-1
M=D

// push constant 16
@16
D=A
@SP
AM=M+1
A=A-1
M=D

// eq
@SP
AM=M-1
D=M
A=A-1
D=M-D
@TRUE1
D;JEQ
@SP
A=M-1
M=0
@STOP1
0;JMP
(TRUE1)
@SP
A=M-1
M=-1
(STOP1)

// push constant 16
@16
D=A
@SP
AM=M+1
A=A-1
M=D

// push constant 17
@17
D=A
@SP
AM=M+1
A=A-1
M=D

// eq
@SP
AM=M-1
D=M
A=A-1
D=M-D
@TRUE2
D;JEQ
@SP
A=M-1
M=0
@STOP2
0;JMP
(TRUE2)
@SP
A=M-1
M=-1
(STOP2)

// push constant 892
@892
D=A
@SP
AM=M+1
A=A-1
M=D

// push constant 891
@891
D=A
@SP
AM=M+1
A=A-1
M=D

// lt
@SP
AM=M-1
D=M
A=A-1
D=M-D
@TRUE3
D;JLT
@SP
A=M-1
M=0
@STOP3
0;JMP
(TRUE3)
@SP
A=M-1
M=-1
(STOP3)

// push constant 891
@891
D=A
@SP
AM=M+1
A=A-1
M=D

// push constant 892
@892
D=A
@SP
AM=M+1
A=A-1
M=D

// lt
@SP
AM=M-1
D=M
A=A-1
D=M-D
@TRUE4
D;JLT
@SP
A=M-1
M=0
@STOP4
0;JMP
(TRUE4)
@SP
A=M-1
M=-1
(STOP4)

// push constant 891
@891
D=A
@SP
AM=M+1
A=A-1
M=D

// push constant 891
@891
D=A
@SP
AM=M+1
A=A-1
M=D

// lt
@SP
AM=M-1
D=M
A=A-1
D=M-D
@TRUE5
D;JLT
@SP
A=M-1
M=0
@STOP5
0;JMP
(TRUE5)
@SP
A=M-1
M=-1
(STOP5)

// push constant 32767
@32767
D=A
@SP
AM=M+1
A=A-1
M=D

// push constant 32766
@32766
D=A
@SP
AM=M+1
A=A-1
M=D

// gt
@SP
AM=M-1
D=M
A=A-1
D=M-D
@TRUE6
D;JGT
@SP
A=M-1
M=0
@STOP6
0;JMP
(TRUE6)
@SP
A=M-1
M=-1
(STOP6)

// push constant 32766
@32766
D=A
@SP
AM=M+1
A=A-1
M=D

// push constant 32767
@32767
D=A
@SP
AM=M+1
A=A-1
M=D

// gt
@SP
AM=M-1
D=M
A=A-1
D=M-D
@TRUE7
D;JGT
@SP
A=M-1
M=0
@STOP7
0;JMP
(TRUE7)
@SP
A=M-1
M=-1
(STOP7)

// push constant 32766
@32766
D=A
@SP
AM=M+1
A=A-1
M=D

// push constant 32766
@32766
D=A
@SP
AM=M+1
A=A-1
M=D

// gt
@SP
AM=M-1
D=M
A=A-1
D=M-D
@TRUE8
D;JGT
@SP
A=M-1
M=0
@STOP8
0;JMP
(TRUE8)
@SP
A=M-1
M=-1
(STOP8)

// push constant 57
@57
D=A
@SP
AM=M+1
A=A-1
M=D

// push constant 31
@31
D=A
@SP
AM=M+1
A=A-1
M=D

// push constant 53
@53
D=A
@SP
AM=M+1
A=A-1
M=D

// add
@SP
AM=M-1
D=M
A=A-1
M=D+M

// push constant 112
@112
D=A
@SP
AM=M+1
A=A-1
M=D

// sub
@SP
AM=M-1
D=M
A=A-1
M=M-D

// neg
@SP
A=M-1
M=-M

// and
@SP
AM=M-1
D=M
A=A-1
M=D&M

// push constant 82
@82
D=A
@SP
AM=M+1
A=A-1
M=D

// or
@SP
AM=M-1
D=M
A=A-1
M=D|M

// not
@SP
A=M-1
M=!M

(END)
@END
0;JMP