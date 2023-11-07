# Assembler
Translating machine language programs from *symbolic* form (assembly) into *binary* form (understood by hardware). The assembler is essentially a *text-processing program*.

### Symbols
Symbols refer to programmer-created aliases for either Memory addresses (**variables**) or sections of instruction code (**labels**). These symbols **only exist on the assembly level**! Binary machine language has no means of understanding them and thus it is the task of the assembler to take care of their management.

### Symbol Resolution
Resolution of variables and labels (or other, additional symbols allowed as per the *assembly-binary contract*) follows pre-specified rules. Commonly, there is a fixed address in Memory that serves as the beginning of the *"symbol space"*, which at the same time serves as the **maximum allowed program length**. 

E.g. Variables may be stored in Memory addresses starting from `1024` onward, this means that:
* address `1024` (and onward up to a specified end) **definitely** holds a variable value as referenced by its symbol in the assembly code
* a generic program can only be a **maximum** of `1024` (starting from `0`) instructions long

#### Symbol Table
Each new symbol in the source code (assembly program) is identified by the assembler and stored in symbol table, which is essentially a *symbol-address mapping* upon its first encounter. This symbol table is then used to replace all symbol references in the source code by its physical Memory address.

E.g.
> i     1024
>
> sum   1025
>
> loop  2

**Note:** In the above example, both `i` & `sum` refer to variables and as such are stored in Memory address `1024+` (following the *Symbol Resolution* example). On the other hand, `loop` refers to a section of the instruction program itself (namely a label to jump to using a `goto` instruction). Therefore, `loop` is mapped to relevant *line of code* to be executed by the goto instruction.

### Translation
Using the agreed-upon rules, the assembler performs the following tasks:

1. Symbol resolution
    * allocated symbols to physical memory
2. Symbol table creation
    * create a look-up table for symbol-memory mapping
3. Replace symbols with memory addresses
4. Translate mnemonic instructions into binary using *machine language specification*
    * assemble binary codes into a complete machine instruction

The assembler must take care of all symbol handling including correct memory allocation. For example, a *single* line assembly instructions may produce binary machine code that is **three words** long; the assembler must be able to account for such a case and handle it accordingly and correctly.

### Python Implementation
Hack assembler written in python 3.10 according to [project 6](../projects/06/) contract specifications.

**Assembler files**
* [assembler](../projects/06/assembler.py) (main)
* [hack_parser](../projects/06/hack_parser.py)
* [comp_codes](../projects/06/comp_codes.py)
* [symbol_table](../projects/06/symbol_table.py)