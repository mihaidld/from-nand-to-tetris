
// function SimpleFunction.test 2
(SimpleFunction.test)
@0
D=A
@SP
AM=M+1
A=A-1
M=D
@0
D=A
@SP
AM=M+1
A=A-1
M=D

// push local 0
@LCL
D=M
@0
D=D+A
@R15
M=D
A=D
D=M
@SP
AM=M+1
A=A-1
M=D

// push local 1
@LCL
D=M
@1
D=D+A
@R15
M=D
A=D
D=M
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

// not
@SP
A=M-1
M=!M

// push argument 0
@ARG
D=M
@0
D=D+A
@R15
M=D
A=D
D=M
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

// push argument 1
@ARG
D=M
@1
D=D+A
@R15
M=D
A=D
D=M
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

// return
@LCL
D=M
@R13
M=D
@5
D=A
@R13
D=M-D
A=D
D=M
@R14
M=D
@ARG
D=M
@0
D=D+A
@R15
M=D
@SP
AM=M-1
D=M
@R15
A=M
M=D
@ARG
D=M+1
@SP
M=D
@1
D=A
@R13
D=M-D
A=D
D=M
@THAT
M=D
@2
D=A
@R13
D=M-D
A=D
D=M
@THIS
M=D
@3
D=A
@R13
D=M-D
A=D
D=M
@ARG
M=D
@4
D=A
@R13
D=M-D
A=D
D=M
@LCL
M=D
@R14
A=M
0;JMP
