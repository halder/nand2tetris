// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)
//
// This program only needs to handle arguments that satisfy
// R0 >= 0, R1 >= 0, and R0*R1 < 32768.

    @prod
    M=0

    @R0         // grab a value
    D=M
    @a
    M=D
    @OUT        // end if a <= 0
    D;JLE

    @R1
    D=M
    @b          // grab b value
    M=D
    @OUT        // end if b <= 0
    D;JLE

    // check which of the two is smaller
    // if: a - b < 0 then a < b (case A)
    // if: a - b > 0 then a > b (case B)
    // if: a - b = 0 then a = b (treat as case A)
    @a
    D=M
    @b
    D=D-M
    
    @A
    D;JLE       // if a <= b, calculate a * b in order to reduce iterations

    @B
    D;JGT       // if a > b, calculate b * a in order to reduce iterations

(A) // a <= b
    (A_LOOP)    // add b to product a times
        @b
        D=M
        @prod
        M=D+M

        @a
        MD=M-1  // a counter and end condition

        @A_LOOP
        D;JGT

        @OUT
        D;JEQ

(B) // a > b
    (B_LOOP)    // a to product b times
        @a
        D=M
        @prod
        M=D+M

        @b
        MD=M-1  // b counter and end condition

        @B_LOOP
        D;JGT

        @OUT
        D;JEQ

(OUT) // store product in RAM[2]
    @prod
    D=M
    @R2
    M=D

(END)
    @END
    0;JMP