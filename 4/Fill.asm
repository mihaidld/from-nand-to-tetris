// Listen to the keyboard 
// Whenever any key is pressed make full screen black, whenever no key is press make it white again

// Pseudo code
// n = 8192 
// addr = SCREEN (base address of screen memory map)
// i = 0 (current index will change)

// Start infinite loop to listen to keyboard
// LISTEN outer loop
// if RAM[KBD] == 0 goto WHITE else continue with BLACK loop

// BLACK inner loop to blacken:
// if i = n goto LISTEN
// RAM[addr] = -1
// addr++ // advances to next register
// i++
// goto BLACK

// WHITE inner loop to whiten:
// if i = n goto LISTEN
// RAM[addr] = 0
// addr++ // advances to next register
// i++
// goto WHITE


@8192
D=A
@n
M=D // n = 8192 (8k size of SCREEN memory map)

(LISTEN)
@i
M=0 // reset i = 0, current index which will change with loop

@SCREEN
D=A
@addr
M=D // reset addr = = 16384, current address inside memory map will change with loop

@KBD
D=M
@WHITE
D;JEQ // goto WHITE loop if KBD stores 0 (no key is pressed) else continue

(BLACK)
@i
D=M
@n
D=M-D
@LISTEN
D;JEQ // when n-i == 0 (i has reached n) we stop loop and go to beginning of outer loop

// blacken all pixels
@addr
A=M
M=-1 // RAM[addr] = -1, or 1111... so all 16 pixels filled
@addr
M=M+1 // addr++
@i
M=M+1 // i++
@BLACK
0;JMP

(WHITE)
@i
D=M
@n
D=M-D
@LISTEN
D;JEQ // when n-i == 0 (i has reached n) we stop loop and go to beginning of outer loop

// whiten all pixels
@addr
A=M
M=0 // RAM[addr] = 0, or 0000... so all 16 pixels white
@addr
M=M+1 // addr++
@i
M=M+1 // i++
@WHITE
0;JMP