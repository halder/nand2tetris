"""Hack assembler command parser module."""

import string

def get_command_type(command):
    if command.startswith("@"):
        command_type = "A_COMMAND"
    else:
        if command.startswith("("):
            command_type = "L_COMMAND"
        else:
            command_type = "C_COMMAND"
    
    return command_type


def get_label(command):
    return command.replace("(", "").replace(")", "")


def get_symbol(command):
    return command.replace("@", "")


def get_c_mnemonics(command):
    if "=" in command:
        dest, comp_jump = command.split("=")
    else:
        dest, comp_jump = None, command
    
    if ";" in comp_jump:
        comp, jump = comp_jump.split(";")
    else:
        comp, jump = comp_jump, None

    return dest, comp, jump


def preprocess_command(command):
    command = command.strip()
    
    # flag for skipping comments and empty lines
    valid_command = True
    if command.startswith("//") or command.isspace() or not command:
        valid_command = False

    # whitespaces are ignored
    for ws in string.whitespace:
        command = command.replace(ws, "")

    # in-line comments are ignored
    if "//" in command:
        command = command.split("//")[0]
    
    return command, valid_command