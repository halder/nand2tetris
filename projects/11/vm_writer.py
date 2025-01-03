class VMWriter:
    def __init__(self, file):
        self.file = file

    def write_push(self, segment, index):
        self.file.write(f"push {segment} {index}\n")

    def write_pop(self, segment, index):
        self.file.write(f"pop {segment} {index}\n")

    def write_arithmetic(self, command):
        self.file.write(f"{command}\n")

    def write_label(self, label):
        self.file.write(f"label {label}\n")

    def write_goto(self, label):
        self.file.write(f"goto {label}\n")

    def write_if(self, label):
        self.file.write(f"if-goto {label}\n")

    def write_call(self, name, n_args):
        self.file.write(f"call {name} {n_args}\n")

    def write_function(self, name, n_args):
        self.file.write(f"function {name} {n_args}\n")

    def write_return(self):
        self.file.write("return\n")
