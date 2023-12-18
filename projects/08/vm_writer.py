from asm_map import ASM

def write_assembly(cmd_type, arg1, arg2, command_cnt, filename, current_function):
    """Write module main function."""
    
    if cmd_type == "C_ARITHMETIC":
        asm_command = __write_arithmetic(arg1, arg2, command_cnt)
    
    elif cmd_type in ("C_POP", "C_PUSH"):
        asm_command = __write_pushpop(cmd_type, arg1, arg2, filename)
    
    elif cmd_type == "C_LABEL":
        asm_command = f"({current_function}${arg1})"

    elif cmd_type == "C_GOTO":
        asm_command = f"\t@{current_function}${arg1}\n\t0;JMP"
    
    elif cmd_type == "C_IF":
        asm_command = "\n\t".join(ASM[cmd_type]).replace("%%IF%%", f"{current_function}${arg1}")
        asm_command = f"\t{asm_command}"

    elif cmd_type == "C_FUNCTION":
        asm_command = "\n\t".join(ASM[cmd_type]).replace("%%FNAME%%", f"{arg1}").replace("%%NLCL%%", f"{arg2}").replace("%%CNT%%", f"{command_cnt}")
        asm_command = asm_command.replace("\n\t(", "\n(")

    elif cmd_type == "C_RETURN":
        asm_command = "\n\t".join(ASM[cmd_type])
        asm_command = f"\t{asm_command}"

    elif cmd_type == "C_CALL":
        asm_command = "\n\t".join(ASM[cmd_type]).replace("%%FNAME%%", f"{arg1}").replace("%%NARG%%", f"{arg2}").replace("%%CNT%%", f"{command_cnt}")
        asm_command = asm_command.replace("\n\t(", "\n(")

    return asm_command


def __concat_asm_commands(cmd_type, tier_type):
    asm_command = "\n\t".join(ASM[cmd_type][tier_type]).replace("\n\t(", "\n(")
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


def __write_arithmetic(arg1, arg2, command_cnt):
    if arg1 in ("add", "sub", "and", "or"):
        op_type = "binary"
    elif arg1 in ("not", "neg"):
        op_type = "unary"
    else:
        op_type = "logic"

    asm_command = __concat_asm_commands("C_ARITHMETIC", op_type)
    
    if op_type == "logic":
        asm_command = asm_command.replace("%%COND%%", f"J{arg1.upper()}")
        asm_command = asm_command.replace("%%COUNT%%", f"{command_cnt}")
    else:
        asm_command = f"{asm_command}\n\tM={ASM['C_ARITHMETIC'][arg1]}"

    return asm_command


def __write_pushpop(cmd_type, arg1, arg2, filename):
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