// Example program
// Flip values stored in RAM[0] and RAM[1]

    // grab content of R0 and store in variable `temp`
    @R0
    D=M
    @temp
    M=D
    
    // grab R1 and store in R0
    @R1
    D=M
    @R0
    M=D

    // grab `temp` (=R0) and store in R1
    @temp
    D=M
    @R1
    M=D

(END)
    @END
    0;JMP