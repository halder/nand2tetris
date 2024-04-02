"""
Optimizations:
    * tokenizer does NOT handle nested comments & "comments" within string constants
"""

import sys
import os

import compilation_engine
import tokenizer

TOKEN_DIR = "tokenized_jack_files"
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

    with open(f"{TOKEN_DIR}/{jack_file.replace('.jack', '.xml')}", "a") as target_file:
        parser = compilation_engine.Parser(list_of_tokens, target_file)

        parser.compile()

        # Note: Subsequent code is used for pre-compilation engine steps to validate tokenizer.        
        #target_file.write("<tokens>\n")
        
        #for token in list_of_tokens:
            #token_type, token_value = token["type"], token["value"]
            #target_file.write(f"\t<{token_type}> {token_value} </{token_type}>\n")
        #target_file.write("</tokens>")
    
    print(f"done w/ file: {jack_file}")
print("done.")