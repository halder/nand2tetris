# Virtualization
Two-tier compilation processes are implemented through ***virtual machines (VM)***, which produce "VM code". This general VM code can then be interpreted on target machines with varying CPU architectures using a **VM translator**. The idea here is to *"write once, run anywhere"*.

VM Code needs to be:
* sufficiently "**high** level" for easy translation from the *source language* to the *VM language*
* sufficiently "**low** level" for easy translation from the *VM language* to the *target machine language*

In order to write a VM translator, one must be familiar with:
* the *source* language
* the *target* language
* the *VM mapping* on the target *platform* (set of rules)
    * how to map VM data structures on host RAM?
    * how to express VM commands in host assembly/machine language?

### Contents
* [VM Abstraction](#vm-abstraction)
    * [The Stack](#the-stack)
    * [Memory Segments](#memory-segments)
* [VM Implementation](#vm-implementation)
    * [Pointer Manipulation](#pointer-manipulation)
    * [Stack Implementation](#stack-implementation)
    * [Memory Implementation](#memory-implementation)
* [Project 7: VM translator I](#vm-to-hack-translator-i)

### VM Abstraction
High level programming languages are an *abstraction*, they do not exist for real. As such, they can be implemented using a VM, particularly a *stack* machine. However, the stack machine is *also an abstraction* itself, which in turn can be implemented by something (not known yet) even more low level.

#### The Stack
The *stack machine* is an abstraction that consists of an *architecture* (Stack) and a *set of operations* (Stack arithmetic) which can applied to the stack.

The stack architecture can be thought of as a stack of plates, where the only **two possible** operations that can be performed are (1) *adding a plate **on top** of the stack* and (2) *removing the **topmost** plate from the stack*.

**Architecture**
- initially **empty** stack
- **stack pointer** pointing to the location to which the **next item** will be added ("*pushed*")
- two operations **only**
    - `push`: Add element to *top* of stack
    - `pop`: Remove *topmost* element from stack

**Arithmetic**
- operations which can be performed on the stack
- no definitive list of operations; operations are coming from the **compiler**
    - i.e. high level language supports a certain operation -> operation translated into VM language
    - ex:
        - high level: x = 17 + 9
        - vm code: push 17; push 9; add; pop x
- examples/common operations:
    - `add`: *pop* the 2 topmost values from stack; *add* them up (**outside of stack**); *push* result onto stack
        - sequence: pop A -> pop B -> A + B (somewhere) -> push (A + B); **THIS SEQUENCE IS IMPLICIT! (no "pop A; pop B" instruction)**
    - `neg`: negate topmost value from stack
        - sequence: pop X -> negate X (somewhere) -> push (NEG X)
    - `eq`: are 2 topmost values equal?
        - pop A -> pop B -> compare (somewhere) -> push A == B
    - `or`: see eq
    - applying **any** `function f` on the stack:
        1. pop argument(s) from stack
        2. compute f on arguments
        3. push result onto stack

#### Memory Segments
High level languages support many different types of variables, for example *local*, *global*, *constants*, *function arguments*, *object instances*, *arrays* etc. In order to preserve the variable "type", i.e. the *name-to-type **mapping***, we need multiple, *different* memory segments which the stack operates on/with.

The different memory segments are then referenced by the *index* holding the relevant value, *as opposed to the variable name*, e.g.:
- push *s1* -> push *static 0*
- push *y*  -> push *argument 1*
- pop *c*   -> pop *local 2*
- push *4*  -> push *constant 4*
- general: `push/pop segment i`

### VM Implementation
The above VM abstraction requires an implemention. In order for it to work, there has to be a mapping/translation "process" similar to how the Assembler translates convenient assembly code into binary machine instructions.

VM memory segments need to be mapped to physical RAM locations/areas ("host RAM"), managed by the VM architecture. VM `push` & `pop` commands need to be translated into machine language; this is achieved by translating them into assembly, which then in turn is translated in to machine language. VM commands operated on the VM memory segments within the host RAM.

#### Pointer Manipulation
Variables that **store memory addresses** are called *pointers*. Elements of the following "pseudo assembly" pointer syntax can be found in modern high level language implementations such as `C`.

**Notation** (pseudo/Hack; transferrable):
| *Syntax <br> (pseudo assembly/high level)* | *Explanation* | *Example* | *Notes* | *Hack implementation* |
| -------- | ------------- | --------- | ------- | --------------------- |
| `*p` | *memory location* that "p" points to | `p = 257` <br> `D = *p` *(== `D = RAM[257]`)* | **asterisk** indicates *"pointing to"* RAM[`p`] | `@p` <br>  `A=M` <br> `D=M` |
| `p--` | **de**crement *actual* value of `p` by 1 | - | `p` now holds value `p-1` | `@p` <br> `M=M-1` |
| `p++` | **in**crement *actual* value of `p` by 1 | - | `p` now holds value `p+1` | `@p` <br> `M=M+1` |
| `*p = 9` | assign value *9* to RAM[`p`] | - | `p` unchanged | `@9` <br> `D=A` <br> `@p` <br> `A=M` <br> `M=D` |

#### Stack Implementation
Both the *stack pointer* and the *stack* itself are located in fixed RAM locations. Beginning of the *stack* is marked by a fixed base address (onward from there). The *stack pointer* always points to the location to which the next element *will be added*; it points to an "empty space" so to speak (abstractedly), **not the stack base address**!

**Stack Notation**
| *VM code* | *Pseudo assembly/high level code* | *Hack assembly code* |
| --------- | -------- | ---------------------- |
| `push constant 17` | `*SP = 17` <br> `SP++` | `@17` <br> `D=A` <br> `@SP` <br> `A=M` <br> `M=D` <br> `@SP` <br> `M=M+1` |

#### Memory Implementation
Similar to the stack implementation, every memory segment has a corresponding *memory segment pointer* and a *memory segment base address*.
All assumptions about memory segments, except the `static` implementation, are **platform agnostic**. The latter relies on Hack assembler specifics.

**local, argument, this (obj), that (array)** segments:
- one segment pointer per memory segment (stored in RAM[1] - RAM[4])
- to access "segment *i*" the offset *i* must be added to the **base address** of the memory segment (different from stack pointer!)
- ex:
    - `pop local i`     -> `addr=LCL+i, SP--, *addr=*SP`
    - `push local i`    -> `addr=LCL+i, *addr=*SP, SP++`

**constant** segment:
- *pseudo* segment, does **not** exist for real in RAM!
- constant memory segment supports only `push` commands and in turn provides the desired constant onto the stack
- ex: `push constant i` -> `*SP=i, SP++`

**static** segment:
- holds class level (**global** space) variables which need to be accessed from all functions of/within the object
- therefore stored in a "common" memory location
    - "commonness" is achieved by *relying on Hack assembler specifics* (how & where variables are stored)
    - this segment's implementation is therefore **not hardware agnostic**
- VM translator translates static references `static i` in a file (== object), e.g. `Foo.vm` into a reference symbol in assembly code `Foo.i` (*filename.static_index*)
    - results in `@Foo.i` in a Hack assembly program
    - assembler then stores variable "*Foo.i*" in RAM[16] - RAM[255]

**temp** segment:
- high level language compiler sometimes relies on creating & using temporary variables
- Hack VM has *8* dedicated slots for temporary variables in RAM[5] to RAM[12]

**pointer** segment:
- needed for the high level language compiler
- keeps track of and supplies the `this` and `that` base addresses
- `push/pop pointer 0/1`
    - pointer 0 = `THIS`
    - pointer 1 = `THAT`

### VM-to-Hack Translator I
VM translator (first stage) written in python 3.10 according to [project 7](../projects/07/) contract specifications.

Implements VM arithmetic & push / pop operations; VM-to-ASM-logic can be found in [vm_command_logic.asm](../projects/07/vm_command_logic.asm).

**VM files**
* [translator](../projects/07/vm_translator.py) (main)
* [parser](../projects/07/vm_parser.py)
* [writer](../projects/07/vm_writer.py)