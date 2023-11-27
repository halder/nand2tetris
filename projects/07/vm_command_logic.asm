// Logic for Hack assembly implementations of VM commands

// ---------------------------------------------------------------------------------------------------------------------------------
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
//// --- C_ARITHMETIC --- //////////////////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// ---------------------------------------------------------------------------------------------------------------------------------
// binary ops:  add, sub, and, or
// unary ops:   neg, not
// logic ops:   eq, gt, lt
// ---------------------------------------------------------------------------------------------------------------------------------
// ---------------------------------------------------------------------------------------------------------------------------------

//// --- add ------------------------------------------------------------------------------------------------------------------ ////
@SP
AM=M-1  // decrement SP (new top of stack after operation) and point to *SP
D=M     // load y into D-register; D=RAM[*SP]
A=A-1   // load address below top of stack into A
M=D+M   // push x+y onto stack

//// --- sub ------------------------------------------------------------------------------------------------------------------ ////
@SP
AM=M-1  // decrement SP (new top of stack after operation) and point to *SP
D=M     // load y into D-register; D=RAM[*SP]
A=A-1   // load address below top of stack into A
M=M-D   // push x-y onto stack

//// --- and ------------------------------------------------------------------------------------------------------------------ ////
@SP
AM=M-1  // decrement SP (new top of stack after operation) and point to *SP
D=M     // load y into D-register; D=RAM[*SP]
A=A-1   // load address below top of stack into A
M=D&M   // push x&y (bitwise) onto stack

//// --- or ------------------------------------------------------------------------------------------------------------------- ////
@SP
AM=M-1  // decrement SP (new top of stack after operation) and point to *SP
D=M     // load y into D-register; D=RAM[*SP]
A=A-1   // load address below top of stack into A
M=D|M   // push x|y (bitwise) onto stack

//// --- not ------------------------------------------------------------------------------------------------------------------ ////
@SP     // note: top of stack before and after operation identical
A=M-1   // load address below top of stack into A
M=!M    // push !y (bitwise) onto stack

//// --- neg ------------------------------------------------------------------------------------------------------------------ ////
@SP     // note: top of stack before and after operation identical
A=M-1   // load address below top of stack into A
M=-M    // push -y onto stack

//// --- eq ------------------------------------------------------------------------------------------------------------------- ////
@SP
AM=M-1  // decrement SP (new top of stack after operation) and point to *SP
D=M     // load y into D-register; D=RAM[*SP]
A=A-1   // load address below top of stack into A
D=M-D   // load x-y into D-register; if x==y, then D==0
M=-1    // assume truth; set default
@SKIP.$$COUNT$$
D;JEQ   // if D==0 then x==y; skip to next command
@SP
A=M-1   // select top of stack
M=0     // if D!=0 then x!=y; falsify
(SKIP.$$COUNT$$)

//// --- gt ------------------------------------------------------------------------------------------------------------------- ////
@SP
AM=M-1  // decrement SP (new top of stack after operation) and point to *SP
D=M     // load y into D-register; D=RAM[*SP]
A=A-1   // load address below top of stack into A
D=M-D   // load x-y into D-register; if x>y, then D>0
M=-1    // assume truth; set default
@SKIP.$$COUNT$$
D;JGT   // if D>0 then x>y; skip to next command
@SP
A=M-1   // select top of stack
M=0     // if D<=0 then x<=y; falsify
(SKIP.$$COUNT$$)


//// --- lt ------------------------------------------------------------------------------------------------------------------- ////
@SP
AM=M-1  // decrement SP (new top of stack after operation) and point to *SP
D=M     // load y into D-register; D=RAM[*SP]
A=A-1   // load address below top of stack into A
D=M-D   // load x-y into D-register; if x<y, then D<0
M=-1    // assume truth; set default
@SKIP.$$COUNT$$
D;JLT   // if D<0 then x<y; skip to next command
@SP
A=M-1   // select top of stack
M=0     // if D>=0 then x>=y; falsify
(SKIP.$$COUNT$$)


// ---------------------------------------------------------------------------------------------------------------------------------
// ---------------------------------------------------------------------------------------------------------------------------------
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
//// --- C_PUSH --- ////////////////////////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// ---------------------------------------------------------------------------------------------------------------------------------
// indirect segments:   local, argument, this, that     --> indirect segments do not occupy fixed registers, their location can vary
// direct segments:     temp, pointer, static           --> direct segments occupy fixed registers in the Hack memory
// virtual segment:     constant
// ---------------------------------------------------------------------------------------------------------------------------------

//// --- indirect ------------------------------------------------------------------------------------------------------------- ////
@i      // here, `i` is an integer referring to the segment index, NOT the variable `i`
D=A
@LCL    // get segment base address; segment pointers @LCL, @ARG, @THIS, @THAT
A=D+M   // set address to segment_base_addr+index_i
D=M     // D=RAM[base_addr+index]
@SP
M=M+1   // increment SP; point to new (after command) top of stack
A=M-1   // A=RAM[SP--]
M=D     // push value of register segment_base_addr+index onto stack; RAM[*SP--]=RAM[base_addr+index]

//// --- direct --------------------------------------------------------------------------------------------------------------- ////
@$$ADDR_SEGMENT_i$$ //  get address of `direct_segment i` (calculated by VM translator);
//                      can be either of @THIS, @THAT (segment: pointer), @R{5+i} (segment: temp), @Filename.i (segment: static)
D=M                 // D=RAM[$$ADDR_SEGMENT_i$$]
@SP
M=M+1               // increment SP; point to new (after command) top of stack
A=M-1               // A=RAM[SP--]
M=D                 // push value of register $$ADDR_SEGMENT_i$$ onto stack; RAM[*SP--]=RAM[$$ADDR_SEGMENT_i$$]

//// --- constant ------------------------------------------------------------------------------------------------------------- ////
@i      // here, `i` is an actual integer, NOT the variable `i`
D=A
@SP
M=M+1   // increment SP; point to new (after command) top of stack
A=M-1   // A=RAM[SP--]
M=D     // push integer i onto stack; RAM[*SP--]=i


// ---------------------------------------------------------------------------------------------------------------------------------
// ---------------------------------------------------------------------------------------------------------------------------------
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
//// --- C_POP --- /////////////////////////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// ---------------------------------------------------------------------------------------------------------------------------------
// indirect segments:   local, argument, this, that     --> indirect segments do not occupy fixed registers, their location can vary
// direct segments:     temp, pointer, static           --> direct segments occupy fixed registers in the Hack memory
// ---------------------------------------------------------------------------------------------------------------------------------

//// --- indirect ------------------------------------------------------------------------------------------------------------- ////
@i      // here, `i` is an integer referring to the segment index, NOT the variable `i`
D=A
@LCL    // get segment base address; segment pointers @LCL, @ARG, @THIS, @THAT
D=D+M   // D=i+RAM[segment_pointer]=2+300=302
@R13    // store pointer to segment_base_addr+i
M=D
@SP
AM=M-1  // decrement SP (new top of stack after operation) and point to *SP
D=M     // D=RAM[*SP]
@R13
A=M     // get pointer and point to segment_base_addr+i
M=D     // RAM[segment_base_addr+i]=RAM[*SP]

//// --- direct --------------------------------------------------------------------------------------------------------------- ////
@SP
AM=M-1              // decrement SP (new top of stack after operation) and point to *SP
D=M                 // D=RAM[*SP]
@$$ADDR_SEGMENT_i$$ //  get address of `direct_segment i` (calculated by VM translator);
//                      can be either of @THIS, @THAT (segment: pointer), @R{5+i} (segment: temp), @Filename.i (segment: static)
M=D                 // RAM[$$ADDR_SEGMENT_i$$]=RAM[*SP]
