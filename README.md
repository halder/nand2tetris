# Nand To Tetris Coursework

![title img](img/simplicity.png)

> *"An idiot admires complexity, a genius admires simplicity."*
>
> &mdash; Terry A. Davis

### Contents
* [Intro](#intro)
* [Simulation (Coursework)](#a-simulation---from-logic-gates-to-the-hack-computer)
    * [Summary (Notes)](#summary)
* [Beyond Simulation](#b-beyond-simulation)
    * [Transistors](#transistors)
    * [FPGAs](#field-programmable-gate-arrays-fpgas)

## Intro
Building a working, **simulated** *16*-bit computer from first principles. Working through the chapters/projects using Coursera.

**Course Resources**
* [Nand2Tetris Website](https://www.nand2tetris.org/)
* [Coursera: Part I](https://www.coursera.org/learn/build-a-computer)
* [Coursera: Part II](https://www.coursera.org/learn/nand2tetris2)
* [HDL Survival Guide](https://www.nand2tetris.org/hdl-survival-guide)

**Supplementary Resources**
* [[YouTube: ***Sebastian Lague***] Exploring How Computers Work](https://www.youtube.com/watch?v=QZwneRb-zqA&ab_channel=SebastianLague)
* [[YouTube: ***Ben Eater***] Building an 8-bit breadboard computer](https://www.youtube.com/playlist?list=PLowKtXNTBypGqImE405J2565dvjafglHU) (*note*: very long)

## A. Simulation - From Logic Gates to the Hack Computer
This is where the journey starts. Building elementary, 16-bit variant (bus input) & multi-way variant logic gates starting from just NAND.

Building upon these basic gates we build the ALU, Memory and eventually the full-blown (albeit **simulated**) Hack computer.

Similarly to the 16-bit computer, 32-bit (64-bit respectively) computers require 32-bit (64-bit) variants of logic gates.

### Summary
|Notes / Programs|Project|
|---|---|
|[**Boolean Logic**](notes/bool.md)|1|
|[**Boolean Functions and Gate Logic**](notes/gates.md)|1|
|[**Boolean Arithmetic and the ALU**](notes/alu.md)|2|
|[**Sequential Logic and Memory**](notes/memory.md)|3|
|[**Machine Language**](notes/machine_lang.md/)|4|
|[**Architecture**](notes/architecture.md)|5|
|[**Assembler**](notes/assembler.md)|6|
|[**Virtual Machine: Architecture**](notes/vm_architecture.md)|7|
|[**Virtual Machine: Flow**](notes/vm_flow.md)|8|
|[**Compiler: Syntax Analysis**](notes/compiler_parser.md)|10|
<!-- |[**Compiler: Code Generation**](notes/compiler_code_gen.md)|11| -->

## B. Beyond Simulation
When it comes to building the Hack computer from real hardware, there are two options:
* Using physical logic gates (e.g. on a breadboard)
* Using Field Programmable Gate Arrays (FPGAs)

At its core, both logic gates and FPGAs are made up of **physical transistors**.

### Transistors
Transistors are the basic building blocks of all logic gates. Although not covered in this course since their inner workings are subject to Physics and Electrical Engineering, understanding how they work is crucial (or at least beneficial) for *really* understanding NAND & logic gates and everything that builds on top of them.

**Resources**
* [[YouTube: ***Lesics***] Transistors, how to they work?](https://www.youtube.com/watch?v=7ukDKVHnac4&ab_channel=Lesics)
* [[YouTube: ***The Engineering Mindset***] Transistors Explained](https://www.youtube.com/watch?v=J4oO7PT_nzQ&ab_channel=TheEngineeringMindset)
* [[YouTube: ***Ben Eater***] Logic Gates from Transistors](https://www.youtube.com/watch?v=sTu3LwpF6XI&list=PLEJ4ZX3tdB692QvbCDnn6wrJGU0kTMY8P&index=2&ab_channel=BenEater)

### Field Programmable Gate Arrays (FPGAs)
[FPGAs](https://en.wikipedia.org/wiki/Field-programmable_gate_array) can be programmed to mimic *any* chip one can think of (within the borders of the actual limitations imposed by the FPGA itself) using Configurable Logic Blocks (CLBs).

**Notes**
* FPGAs **cannot** process *analog* signals - limited to *digital* domain
* large numbers of CLBs possible, which are programmable and can mimic *any* logic gate
    * using Look-Up Tables (LUTs) - think: [Truth tables](https://en.wikipedia.org/wiki/Truth_table#Binary_operations)
* programmable using a HDL such as [Verilog](https://en.wikipedia.org/wiki/Verilog) or [VHDL](https://en.wikipedia.org/wiki/VHDL)

**Resources**
* [[YouTube: ***EEVblog***] What is an FPGA?](https://www.youtube.com/watch?v=gUsHwi4M4xE&ab_channel=EEVblog)
* [[YouTube: ***Charles Clayton***] What is an FPGA?](https://www.youtube.com/watch?v=iHg0mmIg0UU&ab_channel=CharlesClayton)
* [[GitHub: ***geohot***] From the Transistor to the Web Browser](https://github.com/geohot/fromthetransistor)
