// Example program
// Set array of length n to -1 in every slot

// Pseudocode
// for (i=0; i<n; i++){
//      arr[i] = -1   
// }

// Suppose arr=100, n=10
// array of length 10 in memory address starting at 100

    // set variables
    @10     // n
    D=A
    @n
    M=D

    @100    // fix array location in memory to address 100 (up until 100+n)
    D=A
    @arr    // pointer holds current relevant array slot (in memory)
    M=D

(LOOP)
    @arr
    AD=M    // set A & D registers to pointer;

    // set current array slot to -1
    M=-1

    // set pointer to next array slot
    @arr
    M=D+1

    // decrement length counter & check END condition
    @n
    MD=M-1
    @LOOP
    D;JGT

(END)
    @END
    0;JMP