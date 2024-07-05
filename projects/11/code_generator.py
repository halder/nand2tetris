"""
Optimizations:
    * tokenizer does NOT handle nested comments & "comments" within string constants
    * compilation functions are very long, this can be (but probably never will be) optimized
    * current error handling extremely verbose
    * lots of branching which could be reduced significantly
    * current implementation is duck type for primitive data types, no type-checking before any operations takes place
    * current implementation does not allow for an arbitrary number of "binary operation concatentation" without parentheses (two terms, one operand)
"""

import sys
import os

import compilation_engine
import tokenizer

TOKEN_DIR = "vm_files"
os.makedirs(TOKEN_DIR, exist_ok=True)

cwd = os.getcwd()
arg = sys.argv[1]

# translate single file
if arg.endswith(".jack"):
    jack_files = [arg]

# translates multiple files in provided directory
else:
    os.makedirs(f"{TOKEN_DIR}/{arg}", exist_ok=True)
    os.chdir(arg)
    dir_files = os.listdir()
    jack_files = [f"{arg}/{file}" for file in dir_files if file.endswith(".jack")]

os.chdir(cwd)

for jack_file in jack_files:
    with open(jack_file, "r") as source_file:
        content = source_file.readlines()
    
    list_of_tokens = tokenizer.get_tokens(content)

    with open(f"{TOKEN_DIR}/{jack_file.replace('.jack', '.vm')}", "w") as target_file:
        print(f"compiling `{jack_file}` to VM code ...")
        parser = compilation_engine.Parser(list_of_tokens, target_file)
        parser.compile()

print("All files compiled to VM code.")
