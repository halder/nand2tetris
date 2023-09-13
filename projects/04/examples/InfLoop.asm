// Example program
// Infinite loop, listen to keyboard input

(LISTEN)
    @24575
    M=0

    @KBD
    D=M
    @LISTEN
    D;JEQ

(PRESS)
    @24575
    M=-1

    @KBD
    D=M
    @LISTEN
    D;JEQ
    @PRESS
    D;JGT