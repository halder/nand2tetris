"""Hack assembler symbol table module."""

import hack_parser

def get_labels(filename):
    """read source file once; add all labels to symbol look-up table."""

    SYMTAB = {
        "SP": format(0, "016b"),
        "LCL": format(1, "016b"),
        "ARG": format(2, "016b"),
        "THIS": format(3, "016b"),
        "THAT": format(4, "016b"),
        "R0": format(0, "016b"),
        "R1": format(1, "016b"),
        "R2": format(2, "016b"),
        "R3": format(3, "016b"),
        "R4": format(4, "016b"),
        "R5": format(5, "016b"),
        "R6": format(6, "016b"),
        "R7": format(7, "016b"), 
        "R8": format(8, "016b"),
        "R9": format(9, "016b"),
        "R10": format(10, "016b"),
        "R11": format(11, "016b"),
        "R12": format(12, "016b"),
        "R13": format(13, "016b"),
        "R14": format(14, "016b"),
        "R15": format(15, "016b"),
        "SCREEN": format(16384, "016b"),
        "KBD": format(24576, "016b"),
    }

    counter_ROM = 0

    with open(f"{filename}.asm", "r") as file:
        for command in file:
            command, valid_command = hack_parser.preprocess_command(command)
            
            if not valid_command:
                continue
            
            command_type = hack_parser.get_command_type(command)
            
            if command_type == "L_COMMAND":
                label = hack_parser.get_label(command)

                if label not in SYMTAB:
                    SYMTAB[label] = format(counter_ROM, "016b")

            elif command_type in ("A_COMMAND", "C_COMMAND"):
                counter_ROM += 1

    return SYMTAB