// Example program
// Computes: RAM[1] = 1 + 2 + 3 + ... + n,
// where n is stored in RAM[0]; n is assumed to be a POSITIVE integer

    // get user input & declare variables
    @R0
    D=M
    @n
    M=D
    @sum
    M=D

(LOOP)
    @n
    D=M-1
    M=D
    @sum
    M=M+D

    @LOOP
    D;JGT

    // store results in RAM[1]
    @sum
    D=M
    @R1
    M=D

(END)
    @END
    0;JMP