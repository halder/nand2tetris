# Nand To Tetris Coursework
Building a working (simulated) *16*-bit computer from first principles. Working through the chapters using videos on Coursera.

**Resources**
* [Nand2Tetris Website](https://www.nand2tetris.org/)
* [Coursera: Part I](https://www.coursera.org/learn/build-a-computer)
* [Coursera: Part II](https://www.coursera.org/learn/nand2tetris2)

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

<!--
---

### Beyond NAND (FPGAs)
Field Programmable Gate Arrays - tbd

* Digital vs analog
* LUTs
* FPGAs
    + [YouTube: *EEVblog*](https://www.youtube.com/watch?v=gUsHwi4M4xE&ab_channel=EEVblog)
    + [YouTube: *Charles Clayton* (short)](https://www.youtube.com/watch?v=iHg0mmIg0UU&ab_channel=CharlesClayton)
    + reprogrammable
    + versatile (can do anything in the digital domain)
    + fast
    + parallel

-->