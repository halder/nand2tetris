# Operating System
The operating system closes gaps between high-level languages and the hardware it runs on. There is basically no way to write high-level programs without background OS support of some kind. Pretty much all modern high-level languages come equipped with a standard library for hardware support.

The OS' main tasks can be categorized into *language extension / standard library* and *system oriented services*.

**Standard library**
- `I/O` functionality
- `string` and `array` classes and functionality
- `math` operations
- *and many more...*

**System oriented services**
- memory management (`alloc`, `dealloc` etc.)
- file system
- I/O drivers
- UI management (shell, windows)
- multi-tasking (multiple programs at the same time)
- networking (internet)
- security
- *and many more...*


### Efficiency Matters
The lower a service (like a `math` or `sys` operation/functionality) is in the software hierarchy, the more it is vital for it to be optimized. If one core, low-level service is implemented (very) inefficiently, everything on top of it - no matter how optimized it is - will also be inefficient.


### Mathematical Operations
**multiplication**
- how to handle "`i'th bit of y == 1`" (y is 16bit)
    - in general: use bit shifting operations (Jack/Hack does not support)
    - N2T: create one **fixed**, `static` array (at startup) that holds value $2^i$ for $i = 0 ... 15$

**division**
- negative numbers
    - divide `abs(x)` by `abs(y)`
    - set sign


### Memory Access
- functionality performing on the host RAM: `peek`, `poke`, `alloc`, `dealloc`
- program accesses RAM via abstractions (objects, variables, arrays, etc.)
- OS written in Jack -> how to access RAM? (similarly, Windows is written in C++)
- requires a hack: "exploit" weakly typed nature of Jack and *"force"* arrays to have a certain base address, in line with the architecture of the Hack computer
    - i.e. `let ram = 0;`, where `ram` is of type `Array`
    - this out-of-the-order assignment sets `ram`s base address on the stack to "0", an address which is **usually not available**
    - this gives the system (programmer) access to the **entire host RAM**


### Heap Management
- use linked list to keep track of *available* heap segments
- initially, entire heap is *available*
- each "free" list (available heap) element is made up of **three** parts:
    - pointer to the next segment (index)
    - `size` of the elements data block (how many items can be stored here) (int)
    - data blocks (array)
- use another hack, similar to that of accessing the entire host RAM
    - `let heap = 2048;`
    - **Jack Array is not used as a data structure but simply a list of pointers!**

**Note**
- the more we recycle memory blocks, the more the "free" list becomes fragmented with many short segments (since dealloc simply appends a previously used block to the end)
    - alloc now has to search gradually more and more segments in order to find a suitable (best) segments
    - `defragmentation` algorithm goes through free list and tries to merge segments into larger segments (OS functionality) -> not part of this course (but can be implemented easily)


### Textual Output
- font bitmap created **once** upon starting the Hack computer
- stored in a `static` array that holds bitmaps for *all* ASCII characters *allowed* on the Hack platform


### Bootstrapping
(aka "booting") The process of loading the *basic software* into the memory of a computer after power-on or general reset, especially the *operating systems* which will then take care of loading other software as needed.

- software is **burned** into ROM of computer (fixed!)
    - in Hack: `ROM[0] = 256` (sets stack pointer), `call Sys.init`
- loads OS kernel
- loads other windows (applications) on OS


---
### Project: Operating System

OS & standard library for the Hack computer written in Jack.

**OS and standard library files**
* [Array](../projects/12/Array.jack)
* [Keyboard](../projects/12/Keyboard.jack)
* [Math](../projects/12/Math.jack)
    * includes `mod` operation
* [Memory](../projects/12/Memory.jack)
* [Output](../projects/12/Output.jack)
* [Screen](../projects/12/Screen.jack)
* [String](../projects/12/String.jack)
    * recursive and non-recursive versions of `int2str`
* [Sys](../projects/12/Sys.jack)
