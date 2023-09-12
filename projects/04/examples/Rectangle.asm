// Example program
// Draws a filled rectangle at the upper left corner of the screen,
// 16 pixels wide and RAM[0] pixels long

    @R0         // grab user input (rectangle length)
    D=M
    @length     // counter for END condition
    M=D

    @SCREEN     // grab SCREEN base address
    D=A
    @address    // keeps track of row to be calculated
    M=D

(LOOP)
    @address    // get current row pointer address
    A=M
    M=-1        // set selected register (first 16 bits of screen row) to black

    @32         // offset per row; screen width / register width (512 / 16)
    D=A
    @address    // update pointer
    M=D+M
    
    @length     // decrement counter
    MD=M-1
    @LOOP
    D;JGT       // end if no more rows to fill

(END)
    @END
    0;JMP