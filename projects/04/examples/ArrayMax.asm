// Example program
// Return maximum value of an array

    // set variables
    @10
    D=A
    @n          // array length; same as length used in Set.asm
    M=D

    @100
    D=A
    @arr        // array location in memory pointer; same as location used in Set.asm
    M=D

    @max        // holds array max value
    M=0

(LOOP)
    @arr        // grab value from current array slot
    A=M
    D=M

    // compare current array value to max value (default 0)
    @max    
    D=D-M
    @UPDATE_MAX // update max if necessary
    D;JGT

(INCREMENT)     // increment array pointer sub-routine
    @arr
    M=M+1

    @n
    MD=M-1

    @LOOP
    D;JGT
    @OUT
    D;JEQ

(UPDATE_MAX)
    @arr        // grab value from current array slot, that is larger than current max
    A=M
    D=M

    @max        // update max
    M=D

    @INCREMENT  // go to next array slot
    0;JMP

(OUT)
    // store max value in register 0
    @max
    D=M
    @R0
    M=D

    @END
    0;JMP

(END)
    @END
    0;JMP