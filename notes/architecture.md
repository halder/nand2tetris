# Computer Architecture
The *von Neumann* architecture and the *Hack* computer.

The basic *von Neumann* architecture is comprised of the following elements:
* **Memory**
    * Program memory (*ROM*)
    * Data memory (*RAM*)
* **CPU**
    * Registers
        * for **interactions** between CPU & Memory
        * stores *Data* and *Addresses*
    * ALU
        * loads information from the *Data* bus and manipulates it using the *Control* bits
* **Buses**
    * information flows between *input*, *CPU*, *Memory* & *output*
    * Control (e.g. *ADD two numbers together*)
    * Address (e.g. *access register 123 to do whatever*)
    * Data (e.g. *value 7*, *result of computation*, ...)

### Fetch-Execute Cycle
The basic CPU loop of executing one instruction after another:

1. **Fetch** an instruction from the Program memory
    * put instruction location in program memory **`address`**
    * get instruction code reading memory at **`address`**
    * *how*: **Program counter** holds **`address`**
2. **Execute** the *fetched* instruction
    * different (sets of) bits from the instruction can hold information for different operations (ALU, access data memory, etc.) to be done in the next execute cycle

### Hardware Organization
A hierarchy of chip parts:
* **Computer**
    * CPU
        * PC (program counter)
            * Adder
            * Elementary logic gates (*ELG*)
        * ALU (arithmetic logic unit)
            * Adder
            * *ELG*
        * Registers
        * *ELG*
    * Memory (RAM unit)
        * Registers
        * *ELG*
    * ROM unit
        * Registers
        * *ELG*

### The Hack Computer
Hack computer architecture & parts as implemented in [Project 5](../projects/05/).

* [Memory](../diagrams/memory.png)
* **CPU** (instruction decoding; data flow is straight forward)
    * [Instruction & load control](../diagrams/cpu_load_control.png)
    * [ALU & PC flow control](../diagrams/cpu_alu_pc_control.png)
* [Computer](../diagrams/computer.png)