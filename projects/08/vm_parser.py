import string
import re

COMMAND_TABLE = {
    "push": "C_PUSH",
    "pop": "C_POP",
    "add": "C_ARITHMETIC",
    "sub": "C_ARITHMETIC",
    "neg": "C_ARITHMETIC",
    "eq": "C_ARITHMETIC",
    "gt": "C_ARITHMETIC",
    "lt": "C_ARITHMETIC",
    "and": "C_ARITHMETIC",
    "or": "C_ARITHMETIC",
    "not": "C_ARITHMETIC",
    "label": "C_LABEL",
    "goto": "C_GOTO",
    "if-goto": "C_IF",
    "function": "C_FUNCTION",
    "call": "C_CALL",
    "return": "C_RETURN",
}


def preprocess_command(command):
    # flag for skipping comments and empty lines
    valid_command = True
    if command.startswith("//") or command.isspace() or not command:
        valid_command = False

    # whitespaces are ignored
    for ws in string.whitespace:
        if ws == " ":
            continue
        command = command.replace(ws, "")

    # in-line comments are ignored
    if "//" in command:
        command = command.split("//")[0]

    command = command.strip()
    
    return command, valid_command


def parse_command(command):
    """Parse module main function."""

    command = re.sub(r"\s+", " ", command)

    cmd_elements = command.split(" ")

    cmd_type = COMMAND_TABLE[cmd_elements[0]]
    arg1 = None
    arg2 = None

    if cmd_type == "C_ARITHMETIC":
        arg1 = cmd_elements[0]
        
    if len(cmd_elements) > 1:
        arg1 = cmd_elements[1]
    if len(cmd_elements) == 3:
        arg2 = int(cmd_elements[2])

    return cmd_type, arg1, arg2