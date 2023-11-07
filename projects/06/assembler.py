"""Hack assembler main module.

- First pass reads assembly file and adds (unseen) `goto` labels (LABEL) to symbol table.
- Second pass reads assembly file again and translates assembly commands into binary machine code.
  Variables (A-instruction commands) are added to symbol table on first sight and subsequently translated using the symbol table.

Whitespace, (inline) comments and labels (on second pass) are ignored.

Variables are stored in memory addresses 16 and onwards.
"""

import sys

import hack_parser
from comp_codes import DEST, JUMP, COMP
import symbol_table

if __name__ == "__main__":
    FILE_NAME = sys.argv[1].split(".")[0]
    counter_RAM = 16

    # first pass
    symtab = symbol_table.get_labels(FILE_NAME)

    # second pass
    with open(f"{FILE_NAME}.hack", "w") as target: 
        with open(f"{FILE_NAME}.asm", "r") as source:
            for command in source: # implicit "advance" parser operation
                command, valid_command = hack_parser.preprocess_command(command)

                if not valid_command:
                    continue


                command_type = hack_parser.get_command_type(command)
                
                # Label commands are ignored in the second pass
                if command_type == "L_COMMAND":
                    continue
                
                # Compute commands
                if command_type == "C_COMMAND":
                    dest, comp, jump = hack_parser.get_c_mnemonics(command)

                    machine_code = f"111{COMP[comp]}{DEST[dest]}{JUMP[jump]}"

                # Address commands
                if command_type == "A_COMMAND":
                    symbol = hack_parser.get_symbol(command)

                    if symbol.isdecimal():
                        mcode = format(int(symbol), "016b")

                    # symbol is variable
                    else:
                        if symbol not in symtab:
                            symtab[symbol] = format(counter_RAM, "016b")

                            counter_RAM += 1
                        
                        mcode = symtab[symbol]

                    machine_code = mcode

                target.write(f"{machine_code}\n")

    print("done.")