# VM: Program Control
Program control consists of two fundamental commands: **Branching** and **function** commands.

- **functions** are abstractions (not part of the original language keywords)
    - basic language can be extended at will
    - extensions are infinite
    - a `function` can be `called` (invoked) and `returns` a certain value
    - implementation does not really matter; can be *used* before being implemented
- **branching** handles jump control
    - `goto`, `if-goto` to a certain `label`
    - branching turns a linear program into one with *non-linear* program flow (**loops**)
- function & branching commands need to be implemented in VM language & assembly (*implementation*)

### Function Commands
A program consists of *many* functions. At a given point of time/in the program, only *a few* functions are executing. These currently executing functions are doing so using a **calling chain**.

E.g. `foo` calls `bar` calls `sqrt` calls `...`

Within the *calling chain*, only the **currently running** function can return a value (**LIFO/stack**). This introduces the notion of a *global stack*. Think of the function calling chain as a *recursive process*.

**Function calling & returning**
- each function has its own **state**/**private world**
    - exists as long as function is part of the calling chain
    - stack, virtual memory segments, pointers, etc. **per** function!
    - upon **returning**, function state (of *callee*) will be recycled / *memory free'd*

- **Caller**
    - e.g. `main`
    - flow:
        - push `n` arguments of *callee* onto stack
        - save **return address** (where does program *continue* once callee is done?)
        - save **current state of memory segments and pointers** (frame)
        - `call` function (callee)
        - **pass** `arguments` to callee (vm does that)
        - callee *return value* **replaces** `n` arguments
        - **reinstate** caller stack & memory
        - **continue** caller flow -> **jump to return address**

- **Callee**
    - e.g. `foo` called from `main`
    - any callee can itself become a caller (**calling chain**)
    - flow:
        - initiate state (vm)
        - handed `n` arguments (through vm)
        - push **return value** onto *callee* stack
        - hand over **return value** to caller (vm; **copy into `argument 0` on caller's stack**)
        - free memory

### VM-to-Hack Translator II
VM translator (second stage) written in python 3.10 according to [project 8](../projects/08/) contract specifications.

Implements VM program flow & function behavior; VM-to-ASM-logic can be found in [vm_asm_logic.asm](../projects/08/vm_asm_logic.asm).

**VM files**
* [translator](../projects/08/vm_translator.py) (main)
* [parser](../projects/08/vm_parser.py)
* [writer](../projects/08/vm_writer.py)
* [vm-to-asm table](../projects/08/asm_map.py)