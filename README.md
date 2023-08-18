# Nand To Tetris Coursework
Building a working (simulated) *16*-bit computer from first principles. Working through the chapters using videos on Coursera.

**Resources**
* [Nand2Tetris Website](https://www.nand2tetris.org/)
* [Coursera: Part I](https://www.coursera.org/learn/build-a-computer)
* [Coursera: Part II](https://www.coursera.org/learn/nand2tetris2)
* [HDL Survival Guide](https://www.nand2tetris.org/hdl-survival-guide)

---

### Transistors
Transistors are the basic building blocks of all logic gates. Although not covered in this course since their inner workings are subject to Physics and Electrical Engineering, I still believe understanding how they work is crucial (or at least beneficial) for *really* understanding NAND gates and everything that builds on top of them.

**Resources**
* [YouTube: *Lesics*](https://www.youtube.com/watch?v=7ukDKVHnac4&ab_channel=Lesics)
* [YouTube: *The Engineering Mindset*](https://www.youtube.com/watch?v=J4oO7PT_nzQ&ab_channel=TheEngineeringMindset)

---

### Logic Gates
This is where the journey starts. Building elementary, 16-bit variant (bus input) & multi-way variant logic gates starting from just NAND.

Similarly, 32-bit (64-bit respectively) computers require 32-bit (64-bit) variants of logic gates.

#### 1. Boolean Logic
* [Notes on boolean logic](bool_notes.md)
* [Truth tables](https://en.wikipedia.org/wiki/Truth_table#Binary_operations)

#### 2. NAND
* [NAND logic explained](https://www.electronics-tutorials.ws/boolean/bool_4.html)
* [NAND from transistors](https://mathcenter.oxford.emory.edu/site/cs170/nandFromTransistors/)

#### 3. Logic Gate Chip Implementations
As implemented using HDL in [project 1](projects/01/).

* [Not](diagrams/not.png)
* [And](diagrams/and.png)
* [Or](diagrams/or.png)
* [Xor](diagrams/xor.png)
* [Mux](diagrams/mux.png)
* [DMux](diagrams/dmux.png)
* [Not16](diagrams/not16.png)
* *And16*, *Or16* and *Mux16* are trivial and similar to *Not16*
* [Or8Way](diagrams/or8way.png)
* [Mux4Way16](diagrams/mux4way16.png)
* [Mux8Way16](diagrams/mux8way16.png)
* [DMux4Way](diagrams/dmux4way.png)
* [DMux8Way](diagrams/dmux8way.png)

#### 4. Boolean Arithmetic
As implemented using HDL in [project 2](projects/02/).

* [HalfAdder](diagrams/halfadder.png) (**Note**: Two half adders are required to build one full adder - hence the name)
* [FullAdder](diagrams/fulladder.png)
* [Add16](diagrams/add16.png)
    * uses two XOR gates to compute the msb output
    * this reduces the number of total gates used compared to a naive, HalfAdder + 15 FullAdder implementation
* [ALU](diagrams/alu.png)
    * uses two *Mux4Way16* to handle input transformations
    * output is routed to **out**, **ng** & **zr** from the final *Mux16*
        * output's msb suffices as an indicator for negative/positive output values
        * output's lowest & highest 8 bits are routed into separate 8-way OR gates to check for 0 output

<!--
---

### Beyond Simulation (FPGAs)
When it comes to building the Hack computer from real hardware, there are two options:

* Using actual logic gates
* Using Field Programmable Gate Arrays (FPGAs)

FPGAs can be programmed to mimic *any* chip one can think of (within the borders of the actual limitations by the FPGA itself) using reprogrammable cores (CLT?).

**Notes**
* FPGAs **cannot** process *analog* signals - limited to *digital* domain
* many, many CLT which are programmable and can mimic *any* logic gate
    * using Look-Up Tables (LUTs) - think: [Truth tables](https://en.wikipedia.org/wiki/Truth_table#Binary_operations)
* programmable using a HDL such as Verilog or VHDL

**Resources**
* [YouTube: *EEVblog*](https://www.youtube.com/watch?v=gUsHwi4M4xE&ab_channel=EEVblog)
* [YouTube: *Charles Clayton*](https://www.youtube.com/watch?v=iHg0mmIg0UU&ab_channel=CharlesClayton)
* [From the Transistor to the Web Browser (geohot)](https://github.com/geohot/fromthetransistor)

-->