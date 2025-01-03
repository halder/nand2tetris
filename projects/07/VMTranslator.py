import sys

import vm_parser
import vm_writer

source_file_path = sys.argv[1]
source_vm_file_name = source_file_path.split(".")[0]
source_vm_file_path = ""

if "/" in source_vm_file_name:
    source_path = source_vm_file_name.split("/")
    source_vm_file_path = "/".join(source_path[:-1])
    source_vm_file_name = source_path[-1]

with open(source_file_path, "r") as source_file:
    with open(f"{source_vm_file_path}/{source_vm_file_name}.asm", "w") as target_file:
        command_count = 0

        for command in source_file:
            command, valid_command = vm_parser.preprocess_command(command)

            if not valid_command:
                continue

            target_file.write(f"\t// {command}\n")
            
            command_type, arg1, arg2 = vm_parser.parse_command(command)
            assembly_instruction = vm_writer.write_assembly(command_type, arg1, arg2, command_count, source_vm_file_name)

            target_file.write(f"{assembly_instruction}\n")

            command_count += 1
        #target_file.write("\n\t".join(["(END)", "@END", "0;JMP"]))

print(f"Successfully translated `{source_vm_file_name}.vm`. Generated `{source_vm_file_name}.asm`.")
