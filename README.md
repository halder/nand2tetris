# Nand To Tetris Coursework

### Contents
* [Intro](#intro)
* [Simulation (Coursework)](#a-simulation---from-logic-gates-to-the-hack-computer)
    * [Summary (Notes)](#summary)
* [Beyond Simulation](#b-beyond-simulation)
    * [Transistors](#transistors)
    * [FPGAs](#field-programmable-gate-arrays-fpgas)

## Intro
Building a working, **simulated** *16*-bit computer from first principles. Working through the chapters/projects using Coursera.

**Resources**
* [Nand2Tetris Website](https://www.nand2tetris.org/)
* [Coursera: Part I](https://www.coursera.org/learn/build-a-computer)
* [Coursera: Part II](https://www.coursera.org/learn/nand2tetris2)
* [HDL Survival Guide](https://www.nand2tetris.org/hdl-survival-guide)

If interested, see also (note: **very long**):
* [[YouTube: ***Ben Eater***] Building an 8-bit breadboard computer](https://www.youtube.com/playlist?list=PLowKtXNTBypGqImE405J2565dvjafglHU)

## A. Simulation - From Logic Gates to the Hack Computer
This is where the journey starts. Building elementary, 16-bit variant (bus input) & multi-way variant logic gates starting from just NAND.

Building upon these basic gates we build the ALU, Memory and eventually the full-blown (albeit **simulated**) Hack computer.

Similarly to the 16-bit computer, 32-bit (64-bit respectively) computers require 32-bit (64-bit) variants of logic gates.

### Summary
|Notes / Programs|Topic|Related Project|
|---|---|---|
|[**Boolean Logic**](notes/bool.md)|[*Boolean Logic*](https://www.nand2tetris.org/_files/ugd/44046b_f2c9e41f0b204a34ab78be0ae4953128.pdf)|1|
|[**Boolean Functions and Gate Logic**](notes/gates.md)|[*Boolean Logic*](https://www.nand2tetris.org/_files/ugd/44046b_f2c9e41f0b204a34ab78be0ae4953128.pdf)|1|
|[**Boolean Arithmetic and the ALU**](notes/alu.md)|[*Boolean Arithmetic*](https://www.nand2tetris.org/_files/ugd/44046b_f0eaab042ba042dcb58f3e08b46bb4d7.pdf)|2|
|[**Sequential Logic and Memory**](notes/memory.md)|[*Sequential Logic*](https://www.nand2tetris.org/_files/ugd/44046b_862828b3a3464a809cda6f44d9ad2ec9.pdf)|3|
|[**Machine Language**](notes/machine_lang.md/)|[*Machine Language*](https://www.nand2tetris.org/_files/ugd/44046b_7ef1c00a714c46768f08c459a6cab45a.pdf)|4|


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