import sys
import os

import compilation_engine
import tokenizer

path = sys.argv[1]
os.chdir(path)
jack_files = [file for file in os.listdir() if file.endswith(".jack")]

for jack_file in jack_files:
    with open(jack_file, "r") as source_file:
        content = source_file.readlines()
    
    list_of_tokens = tokenizer.get_tokens(content)

    with open(f"{jack_file.replace('.jack', '.vm')}", "w") as target_file:
        print(f"compiling `{jack_file}` to VM code ...")
        parser = compilation_engine.Parser(list_of_tokens, target_file)
        parser.compile()

print("All files compiled to VM code.")
