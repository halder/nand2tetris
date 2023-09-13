// Example program
// Create array of length 10 and fill with values stored in registers 0-9
// Array of length 10 in memory address starting at 100

    // set variables
    @10     // array length
    D=A
    @n
    M=D
    
    @100    // fix array location in memory to address 100 (up until 100+n-1)
    D=A
    @arr    // pointer holds current relevant array slot (in memory)
    M=D

(LOOP)
    @n      // use n as pointer to grab value to be stored from
    A=M-1

    D=M     // load value from R0-9 into data register

    @arr    // get current array pointer
    A=M

    M=D     // store value in array slot

    // set pointer to next array slot
    @arr
    M=M+1

    // decrement length counter & check END condition
    @n
    MD=M-1
    @LOOP
    D;JGT

(END)
    @END
    0;JMP