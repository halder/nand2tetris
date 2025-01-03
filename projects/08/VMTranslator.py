import sys
import os

import vm_parser
import vm_writer
from asm_map import GLOBALS

def write_global_asm(bootstrap_command):
    return "\n\t".join(GLOBALS[bootstrap_command]).replace("\n\t(", "\n(")

source_path = sys.argv[1]

if source_path.endswith(".vm"):
    is_single_file = True
    file_name = source_path.split("/")[-1].split(".")[0]
else:
    is_single_file = False
    file_name = source_path.split("/")[-1]

go_to_path = "/".join(source_path.split("/")[:-1])
if go_to_path:
    os.chdir(go_to_path)

if is_single_file:
    vm_files = [f"{file_name}.vm"]
else:
    os.chdir(file_name)
    vm_files = [file for file in os.listdir() if file.endswith(".vm")]

with open(f"{file_name}.asm", "w") as target_asm_file:
    if not is_single_file:
        target_asm_file.write(f"\t{write_global_asm('JUMP_INIT')}\n")
        target_asm_file.write(f"\t{write_global_asm('SAVE_FRAME')}\n")
        target_asm_file.write(f"\t{write_global_asm('FUNC_RETURN')}\n")
        target_asm_file.write(f"{write_global_asm('SYS_INIT')}\n")

    command_count = 0
    current_function = None

    for vm_file in vm_files:
        vm_file_name = vm_file.split(".")[0]
        with open(vm_file, "r") as source_vm_file:
            for command in source_vm_file:
                command, valid_command = vm_parser.preprocess_command(command)

                if not valid_command:
                    continue
                
                target_asm_file.write(f"\t// {command}\n")

                command_type, arg1, arg2 = vm_parser.parse_command(command)
                if command_type == "C_FUNCTION":
                    current_function = arg1

                assembly_instruction = vm_writer.write_assembly(command_type, arg1, arg2, command_count, vm_file_name, current_function, is_single_file)

                target_asm_file.write(f"{assembly_instruction}\n")

                command_count += 1
    
    target_asm_file.write(write_global_asm("HALT"))
print("done.")
