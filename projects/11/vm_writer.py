from io import TextIOWrapper


class VMWriter:
    def __init__(self, file: TextIOWrapper) -> None:
        self.file = file

    def write_push(self, segment: str, index: int) -> None:
        self.file.write(f"push {segment} {index}\n")

    def write_pop(self, segment: str, index: str) -> None:
        self.file.write(f"pop {segment} {index}\n")

    def write_arithmetic(self, command: str) -> None:
        self.file.write(f"{command}\n")

    def write_label(self, label: str) -> None:
        self.file.write(f"label {label}\n")

    def write_goto(self, label: str) -> None:
        self.file.write(f"goto {label}\n")

    def write_if(self, label: str) -> None:
        self.file.write(f"if-goto {label}\n")

    def write_call(self, name: str, n_args: int) -> None:
        self.file.write(f"call {name} {n_args}\n")

    def write_function(self, name: str, n_args: int) -> None:
        self.file.write(f"function {name} {n_args}\n")

    def write_return(self) -> None:
        self.file.write("return\n")
