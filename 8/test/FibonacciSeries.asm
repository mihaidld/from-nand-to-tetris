
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

// pop pointer 1           
@SP
AM=M-1
D=M
@4
M=D

// push constant 0         
@0
D=A
@SP
AM=M+1
A=A-1
M=D

// pop that 0              
@THAT
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

// push constant 1
@1
D=A
@SP
AM=M+1
A=A-1
M=D

// pop that 1
@THAT
D=M
@1
D=D+A
@R15
M=D
@SP
AM=M-1
D=M
@R15
A=M
M=D

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

// push constant 2         
@2
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

// pop argument 0
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

// label LOOP
(Initial$LOOP)

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

// if-goto COMPUTE_ELEMENT 
@SP
AM=M-1
D=M
@Initial$COMPUTE_ELEMENT
D;JNE

// goto END                
@Initial$END
0;JMP

// label COMPUTE_ELEMENT
(Initial$COMPUTE_ELEMENT)

// push that 0
@THAT
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

// push that 1
@THAT
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

// pop that 2
@THAT
D=M
@2
D=D+A
@R15
M=D
@SP
AM=M-1
D=M
@R15
A=M
M=D

// push pointer 1
@4
D=M
@SP
AM=M+1
A=A-1
M=D

// push constant 1
@1
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

// pop pointer 1
@SP
AM=M-1
D=M
@4
M=D

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

// push constant 1
@1
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

// pop argument 0
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

// goto LOOP
@Initial$LOOP
0;JMP

// label END
(Initial$END)
