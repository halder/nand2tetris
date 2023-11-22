ASM_CMD = {
    "C_ARITHMETIC": {
        "binary":   ["@SP", "AM=M-1", "D=M", "A=A-1"],
        "unary":    ["@SP", "A=M-1"],
        "logic": [
            "@SP", "AM=M-1", "D=M", "A=A-1", "D=M-D", "M=-1", "@SKIP.%%COUNT%%",
            "D;%%COND%%", "@SP", "A=M-1", "M=0", "(SKIP.%%COUNT%%)"
        ],
        "add":  "D+M",
        "sub":  "M-D",
        "and":  "D&M",
        "or":   "D|M",
        "not":  "!M",
        "neg":  "-M"
    },

    "C_PUSH": {
        "end":      ["@SP", "M=M+1", "A=M-1", "M=D"],
        "indirect": ["@%%CONST%%", "D=A", "@%%SEG%%", "A=D+M", "D=M"],
        "direct":   ["@%%ADDR%%", "D=M"],
        "constant": ["@%%CONST%%", "D=A"]
    },
    
    "C_POP": {
        "indirect": [
            "@%%CONST%%", "D=A", "@%%SEG%%", "D=D+M", "@R13", "M=D", "@SP",
            "AM=M-1", "D=M", "@R13", "A=M", "M=D"
        ],
        "direct": ["@SP", "AM=M-1", "D=M", "@%%ADDR%%", "M=D"]
    }
}


def __concat_asm_commands(cmd_type, tier_type):
    asm_command = "\n\t".join(ASM_CMD[cmd_type][tier_type]).replace("\n\t(", "\n(")
    return f"\t{asm_command}"


def __get_indirect_addr_replacement(arg1):
    segment_asm = {
        "local": "LCL",
        "argument": "ARG",
        "this": "THIS",
        "that": "THAT"
    }
    return segment_asm[arg1]


def __get_direct_addr_replacement(arg1, arg2, filename):
    segment_asm = {
        "temp":     f"{5+arg2}",
        "pointer":  "THIS" if arg2 == 0 else "THAT",
        "static":   f"{filename}.{arg2}"
    }
    return segment_asm[arg1]


def __set_addr_replacement(command, segment_type, const=None, seg=None, addr=None):
    if segment_type == "indirect":
        asm_command = command.replace("%%CONST%%", const).replace("%%SEG%%", seg)
    elif segment_type == "direct":
        asm_command = command.replace("%%ADDR%%", addr)
    else:
        asm_command = command.replace("%%CONST%%", const)

    return asm_command


def write_assembly(cmd_type, arg1, arg2, command_cnt, filename):
    """Write module main function."""
    
    if cmd_type == "C_ARITHMETIC":
        if arg1 in ("add", "sub", "and", "or"):
            op_type = "binary"
        elif arg1 in ("not", "neg"):
            op_type = "unary"
        else:
            op_type = "logic"

        asm_command = __concat_asm_commands(cmd_type, op_type)
        
        if op_type == "logic":
            asm_command = asm_command.replace("%%COND%%", f"J{arg1.upper()}")
            asm_command = asm_command.replace("%%COUNT%%", f"{command_cnt}")
        else:
            asm_command = f"{asm_command}\n\tM={ASM_CMD[cmd_type][arg1]}"

    elif cmd_type in ("C_PUSH", "C_POP"):
        const, seg, addr = None, None, None

        if arg1 in ("local", "argument", "this", "that"):
            segment_type = "indirect"
            const = f"{arg2}"
            seg = __get_indirect_addr_replacement(arg1)
        
        elif arg1 in ("temp", "pointer", "static"):
            segment_type = "direct"
            addr = __get_direct_addr_replacement(arg1, arg2, filename)

        else:
            segment_type = "constant"
            const = f"{arg2}"

        asm_command = __concat_asm_commands(cmd_type, segment_type)

        if cmd_type == "C_PUSH":
            asm_command = f"{asm_command}\n{__concat_asm_commands(cmd_type, 'end')}"
        
        asm_command = __set_addr_replacement(asm_command, segment_type, const, seg, addr)

    return asm_command