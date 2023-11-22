import sys
import os

import vm_parser
import vm_writer

cwd = os.getcwd()
arg = sys.argv[1]

# translate single file
if arg.endswith(".vm"):
    vm_files = [arg]

# translates multiple files in provided directory
else:
    os.chdir(arg)
    dir_files = os.listdir()
    vm_files = [file for file in dir_files if file.endswith(".vm")]

os.chdir(cwd)

for vm_file in vm_files:
    with open(vm_file, "r") as source_file:
        filename = vm_file.split(".")[0]

        with open(f"{filename}.asm", "a") as target_file:
            command_cnt = 0

            for command in source_file:
                command, valid_command = vm_parser.preprocess_command(command)

                if not valid_command:
                    continue
                
                target_file.write(f"\t// {command}\n")

                cmd_type, arg1, arg2 = vm_parser.parse_command(command)
                
                assembly_instruction = vm_writer.write_assembly(cmd_type, arg1, arg2, command_cnt, filename)

                target_file.write(f"{assembly_instruction}\n")

                command_cnt += 1

            target_file.write("\n\t".join(["(END)", "@END", "0;JMP"]))

    print(f"done w/ file: {vm_file}")
print("done.")