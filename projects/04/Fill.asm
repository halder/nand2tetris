// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

    @KBD    // for end-of-fill condition; store KBD address in variable in order to 
    D=A     // not interfere with button presses.
    @max    // Probably not necessary, but cleaner anyway.
    M=D

(LISTEN)
    @KBD
    D=M

    @WHITE  
    D;JEQ
    @BLACK
    D;JGT

    // store color in order to have only one FILL loop
    (WHITE)
        @color
        M=0

        @FILL
        0;JMP

    (BLACK)
        @color
        M=-1

        @FILL
        0;JMP

(FILL)
    // reset pointer
    @SCREEN
    D=A
    @addr
    M=D

    (LOOP)
        @color  // get color (0 = white, -1 = black)
        D=M

        @addr   // set screen address to pointer
        A=M

        M=D     // set color of register

        @addr   // begin: check if end of screen reached
        D=M
        @max
        D=M-D

        D=D-1   // do this is instead of ADDRESS=MAX in order to avoid screen filling to set KBD register to -1
                // since it will get stuck in an infinite "-1 loop"

        @LISTEN
        D;JEQ   // end: check if end of screen reached

        @addr
        M=M+1   // increment screen address pointer

        @LOOP
        D;JGT