// SP=256
@256
D=A
@SP
M=D

// call Sys.Init
@Initial$ret0
D=A
@SP
AM=M+1
A=A-1
M=D
@LCL
D=M
@SP
AM=M+1
A=A-1
M=D
@ARG
D=M
@SP
AM=M+1
A=A-1
M=D
@THIS
D=M
@SP
AM=M+1
A=A-1
M=D
@THAT
D=M
@SP
AM=M+1
A=A-1
M=D
@5
D=A
@SP
D=M-D
@ARG
M=D
@SP
D=M
@LCL
M=D
@Sys.init
0;JMP
(Initial$ret0)

// function Main.fibonacci 0
(Main.fibonacci)

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

// lt
@SP
AM=M-1
D=M
A=A-1
D=M-D
@Main.fibonacci$TRUE0
D;JLT
@SP
A=M-1
M=0
@Main.fibonacci$STOP0
0;JMP
(Main.fibonacci$TRUE0)
@SP
A=M-1
M=-1
(Main.fibonacci$STOP0)

// if-goto N_LT_2
@SP
AM=M-1
D=M
@Main.fibonacci$N_LT_2
D;JNE

// goto N_GE_2
@Main.fibonacci$N_GE_2
0;JMP

// label N_LT_2               
(Main.fibonacci$N_LT_2)

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

// label N_GE_2               
(Main.fibonacci$N_GE_2)

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

// call Main.fibonacci 1  
@Main.fibonacci$ret1
D=A
@SP
AM=M+1
A=A-1
M=D
@LCL
D=M
@SP
AM=M+1
A=A-1
M=D
@ARG
D=M
@SP
AM=M+1
A=A-1
M=D
@THIS
D=M
@SP
AM=M+1
A=A-1
M=D
@THAT
D=M
@SP
AM=M+1
A=A-1
M=D
@6
D=A
@SP
D=M-D
@ARG
M=D
@SP
D=M
@LCL
M=D
@Main.fibonacci
0;JMP
(Main.fibonacci$ret1)

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

// call Main.fibonacci 1  
@Main.fibonacci$ret2
D=A
@SP
AM=M+1
A=A-1
M=D
@LCL
D=M
@SP
AM=M+1
A=A-1
M=D
@ARG
D=M
@SP
AM=M+1
A=A-1
M=D
@THIS
D=M
@SP
AM=M+1
A=A-1
M=D
@THAT
D=M
@SP
AM=M+1
A=A-1
M=D
@6
D=A
@SP
D=M-D
@ARG
M=D
@SP
D=M
@LCL
M=D
@Main.fibonacci
0;JMP
(Main.fibonacci$ret2)

// add                    
@SP
AM=M-1
D=M
A=A-1
M=D+M

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

// function Sys.init 0
(Sys.init)

// push constant 4
@4
D=A
@SP
AM=M+1
A=A-1
M=D

// call Main.fibonacci 1
@Sys.init$ret3
D=A
@SP
AM=M+1
A=A-1
M=D
@LCL
D=M
@SP
AM=M+1
A=A-1
M=D
@ARG
D=M
@SP
AM=M+1
A=A-1
M=D
@THIS
D=M
@SP
AM=M+1
A=A-1
M=D
@THAT
D=M
@SP
AM=M+1
A=A-1
M=D
@6
D=A
@SP
D=M-D
@ARG
M=D
@SP
D=M
@LCL
M=D
@Main.fibonacci
0;JMP
(Sys.init$ret3)

// label END
(Sys.init$END)

// goto END  
@Sys.init$END
0;JMP
