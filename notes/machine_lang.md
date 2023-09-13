# Machine Language
Machine language programs run directly on the hardware (CPU) and as such has to be tightly knit to and designed together with the hardware - especially the ALU and its limitations - itself.
Computers only understand bits, i.e. 0's and 1's; Machine language programs are sets of instructions to the computer which are executed in a sequential fashion.

Since it is very cumbersome (and impractical) to write programs as sets of 16-bit sequential instructions, machine language is written in a [mnemonic form](https://en.wikipedia.org/wiki/Assembly_language#:~:text=Assembly%20language%20uses%20a%20mnemonic,to%20form%20a%20complete%20instruction.).

The machine language specifies *all* possible instructions which can be performed on the **particular CPU it is tied to**.

### Operations
Possible operations are limited only by the CPU capabilities and architect decisions (hardware vs. software trade-offs).

An incomplete list of operations defined in the machine language:
* Arithmetic
    * add, substract, ...
* Logical
    * and, or, ...
* Flow Control
    * goto, if A then goto B

### Differences between Machine Languages
* Set of operations (multiplication/division hardware or software?)
* Data types
    * width (e.g. native 64-bit addition vs. 8 * 8-bit addition)
    * floating point, ...

### Hack Programs
[Project 4](../projects/04/), lecture examples & custom programs in order to get a better understanding of assembly programming in the Hack language.

**Project**
* [Fill](../projects/04/Fill.asm)
    * two loops (listen & fill) only; store & grab color selection in dedicated variable
* [Mult](../projects/04/Mult.asm)
    * checks which of `a`, `b` is smaller in order to reduce number of iterations
    
**Arrays**
* [ArraySet](../projects/04/examples/ArraySet.asm)
    * Creates an array of length 10 from values in registers 0-9
* [ArrayMax](../projects/04/examples/ArrayMax.asm)
    * Returns maximum value of an array
    * Array is to be set using `ArraySet.asm` first (or manually)
    * Array resides in RAM[100] - RAM[109]

**Examples**
* [Flip](../projects/04/examples/Flip.asm)
* [Signum](../projects/04/examples/Signum.asm)
* [Sum1toN](../projects/04/examples/Sum1toN.asm)
* [Array](../projects/04/examples/Array.asm)
* [Rectangle](../projects/04/examples/Rectangle.asm)
* [InfLoop](../projects/04/examples/InfLoop.asm)