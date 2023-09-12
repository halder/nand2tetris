// Example program
// Branching, computes:
//     if R0 > 0 then R1 = 1
//     else R1 = 0

    @R0
    D=M
    @GREATER
    D;JGT

    // Less than or equal to 0
    @R1
    M=0
    @END
    0;JMP

(GREATER)
    @R1
    M=1

(END)
    @END 
    0;JMP