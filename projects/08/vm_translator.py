import sys
import os

import vm_parser
import vm_writer
from asm_map import GLOBALS

def write_global_asm(command):
    return "\n\t".join(GLOBALS[command]).replace("\n\t(", "\n(")


cwd = os.getcwd()
arg = sys.argv[1]

# translate single file
if arg.endswith(".vm"):
    single_file = True
    asm_filename = f"{arg.split('/')[-1].split('.vm')[0]}.asm"
    vm_files = [arg]
    arg = "/".join(arg.split("/")[:-1])

# translates multiple files in provided directory
else:
    single_file = False
    asm_filename = f"{arg.split('/')[-1]}.asm"
    os.chdir(arg)
    dir_files = os.listdir()
    vm_files = [f"{arg}/{file}" for file in dir_files if file.endswith(".vm")]

os.chdir(cwd)

with open(f"{arg}/{asm_filename}", "a") as target_file:
    target_file.write(f"\t{write_global_asm('JUMP_INIT')}\n")
    target_file.write(f"{write_global_asm('SAVE_FRAME')}\n")
    target_file.write(f"{write_global_asm('FUNC_RETURN')}\n")
    target_file.write(f"{write_global_asm('SYS_INIT')}\n")
    
    command_cnt = 0
    current_function = None
    
    for vm_file in vm_files:
        with open(vm_file, "r") as source_file:

            for command in source_file:
                command, valid_command = vm_parser.preprocess_command(command)

                if not valid_command:
                    continue
                
                target_file.write(f"\t// {command}\n")

                cmd_type, arg1, arg2 = vm_parser.parse_command(command)
                if cmd_type == "C_FUNCTION":
                    current_function = arg1

                assembly_instruction = vm_writer.write_assembly(cmd_type, arg1, arg2, command_cnt, vm_file.split("/")[-1].split(".")[0], current_function)
        
                target_file.write(f"{assembly_instruction}\n")

                command_cnt += 1

    target_file.write(write_global_asm("HALT"))


    print(f"done w/ file: {vm_file}")
print("done.")