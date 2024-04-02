# Compiler: Syntax Analysis
Much like the VM translator, writing a compiler for a programming language is a two-fold process. First, a *syntax analyzer* retrieves the individual tokens of the program and parses them according to the language's grammar. Next, a *code generator* creates the target VM code.

For Nand2Tetris this compiler turns `Jack` programs into `VM code`. A real world example would be a C compiler which compiles `C` code down to `IR` (down to machine code), e.g. using the `LLVM` backend.

### Lexical Analysis
A lexer is tasked with *tokenizing* & *parsing* the source program. It is working based on the contract of the source language, i.e. its *grammar*.

**1. Tokenizing**

Handles the compiler input, i.e. the *source program*. Supplies the current token's *value and type*. Turns stream of characters (in source program) into *meaningful* tokens (w.r.t. to the source language). Once the input file is "loaded" into the tokenizer, the former is not needed anymore.

A **token** is a sequence of characters that make sense in the programming language.
- e.g. `x++` is meaningful in `C` but **not** in `Python` (equiv. operator `+=`)

This requires the source language to be well-defined:
- keywords
- symbols (`+`, `-`, `=`, `,`, `;`, etc.)
- integer constants
- string constants
- identifiers (variable names)

**2. Grammars**

By itself, a valid set of tokens **does not automatically correspond** to a valid *program* (executable without any errors). A valid program requires **grammar**.

Grammar is a set of rules describing how tokens can be combined to make *meaningful statements in the source language*.

Definitions:
- *LL grammar*: can be parsed by recursive descent parser **WITHOUT** backtracking
- *LL(k) parser*: parser that needs to look *ahead* **AT MOST** *k* tokens in order to determine which rule is applicable
    
**3. Parsing**

A parser determines whether a given input *conforms* to a certain grammar. While parsing, the parser uncovers the entire grammatical structure of the given input.

A parser may output a *parse tree* which describes the input's grammatical structure using a *tree structure*. The *grammatical structure* is represented in the tree's **branches**, while the **leaf nodes** represent the individual *tokens*.

Parse trees can be displayed using *XML* files. Logically, parsers work in a *recursive* fashion, e.g. `compileWhileStatement` might have to call `compileExpression` might have to call `compileTerm` etc.


### Jack Compiler I
Compiler (first stage) written in python 3.10 according to [project 10](../projects/10/) contract specifications, visualized in [Jack grammar flow chart](../documents/jack_grammar.pdf).

**Syntax Analyzer**
* [analyzer](../projects/10/analyzer.py) (main)
    * usage `python3 analyzer.py (DIR_NAME | FILE_NAME.jack)`
* [tokenizer](../projects/10/tokenizer.py)
* [parser](../projects/10/compilation_engine.py)