// Logic for Hack assembly implementations of VM commands

// ---------------------------------------------------------------------------------------------------------------------------------
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
//// --- PROGRAM FLOW --- //////////////////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// ---------------------------------------------------------------------------------------------------------------------------------

//// --- label ---------------------------------------------------------------------------------------------------------------- ////
(functionName$label)

//// --- goto ----------------------------------------------------------------------------------------------------------------- ////
@GOTO_LOCATION
0;JMP

//// --- if ------------------------------------------------------------------------------------------------------------------- ////
@SP
AM=M-1
D=M
@IF_GOTO_LOCATION
D;JNE

// ---------------------------------------------------------------------------------------------------------------------------------
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
//// --- FUNCTION CALLING --- //////////////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// ---------------------------------------------------------------------------------------------------------------------------------

//// --- call ----------------------------------------------------------------------------------------------------------------- ////
    @arg2
    D=A
    @R13    // accessed by __GLOB_SAVE_FRAME
    M=D
    @functionName$__FUNCTION_CALL
    D=A
    @R14    // accessed by __GLOB_SAVE_FRAME
    M=D
    @functionName$ret_n
    D=A     // implicitly accessed by __GLOB_SAVE_FRAME
    @__GLOB_SAVE_FRAME  // jump to global subroutine
    0;JMP
(functionName$__FUNCTION_CALL)  // return here after global subroutine
    @functionName       // jump to called function
    0;JMP
(functioName$ret_n)     // return here after function returns


// global subroutine (used by all calls)
(__GLOB_SAVE_FRAME)
    @SP
    M=M+1
    A=M-1
    M=D                     // push return-address onto stack
    @LCL
    D=M
    @SP
    M=M+1
    A=M-1
    M=D                     // push LCL onto stack
    @ARG
    D=M
    @SP
    M=M+1
    A=M-1
    M=D                     // push ARG onto stack
    @THIS
    D=M
    @SP
    M=M+1
    A=M-1
    M=D                     // push THIS onto stack
    @THAT
    D=M
    @SP
    M=M+1
    A=M-1
    M=D                     // push THAT onto stack
    @R13                    // holds `n`
    D=M
    @5
    D=D+A                   // n+5
    @SP
    D=M-D
    @ARG                    // set arg 0
    M=D
    @SP
    D=M
    @LCL                    // reset LCL
    M=D
    @R14                    // holds `functionName$__FUNCTION_CALL` address
    A=M
    0;JMP

//// --- function ------------------------------------------------------------------------------------------------------------- ////
// if k > 0
(functionName)
    @arg2               // k
    D=A
(__INIT_LCL_x)
    @SP
    M=M+1
    A=M-1
    M=0
    @__INIT_LCL_x
    D=D-1;JGT

// else
(functionName)

//// --- return --------------------------------------------------------------------------------------------------------------- ////
// global subroutine (used by all returns)
(__GLOB_FUNCTION_RETURN)
    @LCL
    D=M
    @R13        // FRAME
    M=D
    @5
    A=D-A       // FRAME-5
    D=M         // return address
    @R14        // RET
    M=D         // RET
    @SP
    A=M-1
    D=M         // get return value
    @ARG
    A=M
    M=D         // RAM[ARG] = return value
    @ARG
    D=M
    @SP
    M=D+1
    @R13        // FRAME
    M=M-1       // FRAME-1
    A=M
    D=M
    @THAT
    M=D
    @R13
    M=M-1       // FRAME-2
    A=M
    D=M
    @THIS
    M=D
    @R13
    M=M-1       // FRAME-3
    A=M 
    D=M
    @ARG
    M=D
    @R13
    M=M-1       // FRAME-4
    A=M
    D=M
    @LCL
    M=D
    @R14
    A=M
    0;JMP

// assembly written by "return"
@__GLOB_FUNCTION_RETURN
0;JMP