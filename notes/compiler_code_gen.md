# Compiler: Code Generation
Each class in a multi-class program written in *Jack* is compiled separately. The code generator takes the [parser output](../notes/compiler_parser.md) and generates valid VM code which runs on the Hack target platform.

### Contents

* [Handling Variables](#handling-variables)
* [Handling Expressions](#handling-expressions)
* [Handling Flow of Control](#handling-flow-of-control)
* [Handling Objects \& Arrays](#handling-objects--arrays)
    * [Construction](#construction)


### Handling Variables

Program-level variable names must be translated into VM code, by translating the high-level mnemonic name into the VM memory segment & index.

Variables have multiple properties:
- name (`identifier`)
- type (`int`, `char`, `bool`, `class` name, ...)
- kind (`field`, `static`, `local`, `argument`) -> VM memory segments (N2T architecture)
- scope (class level vs. subroutine level)

Translation process is done using a symbol table, similar to how the [assembler](../projects/06/symbol_table.py) translates Hack assembly to binary. The Jack programming languages requires only **two** symbol tables to be used when translating to VM language:
- `class` level
- **current** `subroutine` level
    - *every* method (e.g. `SomeClass.get()`) requires as the first entry to the symbol table: `this` -> `argument 0`
    - this is **implicit**, referencing the object *instance* the method is called on
- symbol tables can be **reset** after each successful class/subroutine compilation

**On Programming Languages**

Different high level programming languages have different properties, such as:
- \# of variable types
- \# of variable kinds
- whether or not *nested scoping* is allowed
    - multiple blocks of code are considered separate scopes within the next higher scope; a variable named `x` can reside in multiple scopes
    - nested scoping is handled using a *linked list* -> one symble table per scope (current scope "hides" scoped behind it)


### Handling Expressions

How can we systematically translate infinitely complex (w.r.t. language constraints) expressions into VM code? We are trying to translate high-level *infix* representation into *postfix* VM code representation using a *parse tree* in the middle.

**Two-stage approach (parse tree):**

- **depth first** tree traversal
- from root node traverse down left-to-right until terminal leaf node
- `push` leafe node value
- backtrack to node
    - if more deeper nodes -> continue
    - if not -> push node -> backtrack
- continue in a recursive fashion

**One-stage approach (N2T "codewrite" algo):**

- if *exp* is **constant** `c`: push `c`
- if *exp* is **variable** `var`: push MAPPING-OF(`var`) (e.g. `var` maps to `local 0`)
- if *exp* is `exp1 op exp2`:
    - `codewrite(exp1)`
    - `codewrite(exp2)`
    - output `op`
- if *exp* is `op exp`:
    - `codewrite(exp)`
    - output `op`
- if *exp* is `f(exp1, exp2, ...)`:
    - `codewrite(exp1)`
    - `codewrite(exp2)`
    - `...`
    - output `call f`

**NOTE:** Operator priority (multiplication before addition/subtraction) is part of the compiler **implementation**, NOT the Jack language!


### Handling Flow of Control

Or, how to handle statements, especially loops and branching commands.

Most importantly, all *label* generations (e.g. `goto LABEL`) by the compiler has to be **unique** in all cases, in order to correctly take care of all labels needed in VM-level branching and nested high level statements. 


### Handling Objects \& Arrays

Local and argument variables are only used/needed by the *currently executing function* or a function higher up in the calling chain waiting for the current function to exectue. Considering the temporary nature of these variables, they are stored in the **stack** section of the target RAM.

Object and array data, on the other hand, are manipulated by currently executing *program*, not just a single function. They have to be accessed at various times throughout the program execution, potentially by different functions. There might also be potentially millions of different objects during a program's execution time. Objects and arrays are stored in **heap** section of the target RAM.

Before accessing objects and arrays using `this` (object) or `that` (array), we need to set the `pointer` word to point to either `this` or `that`.

**Note:** Void methods return `0` to the caller, which in turn is being popped into the `temp` memory segment for good.

**!Important:** Both `this` and `that` behave identically. The distinction of `this` for *objects* and `that` for *arrays* is merely a **convention**! The VM architecture of N2T and its virtual memory segments (in particular `this`, `that` and `pointer`) are set up to operate on this distinction, which removes certain ambiguity when handling objects vs. arrays.


#### Construction

Object construction is a caller-callee relationship. Variable declarations allocate a *pointer* to the *object's memory base address* on the **stack** to be used by the subroutine. The object itself is created on the **heap** by the *constructor*.

Using the variable declaration (via the *subroutine symbol table*) the constructor "knows" how much memory space it needs in order to correctly create the object. *Finding* **free** memory space of the required **size** on the target RAM is done by calling `Memory.alloc` (implmentation follows in Ch.12). Furthermore, the constructor initializes the object to some value (on the heap).

Constructor *must* `return this`, therefore return the base address of the selected memory space to the caller and storing it in the *variable pointer* on the stack.


---
### Project: Jack Compiler II

Compiler (second stage) written in python 3.10 according to [project 11](../projects/11/) contract specifications.

**Full-scale Compiler**
* [compiler](../projects/11/compiler.py) (main)
    * usage `python3 compiler.py (DIR_NAME | FILE_NAME.jack)`
* [parser](../projects/11/compilation_engine.py)
* [vm_writer](../projects/11/vm_writer.py)
* [symbol_table](../projects/11/symbol_table.py)
* [tokenizer](../projects/10/tokenizer.py) (unchanged from project 10)
