class SymbolTable:
    # class scope: static, field
    # subroutine scope: arg, var

    def __init__(self) -> None:
        self.i = {"static": 0, "field": 0, "arg": 0, "var": 0}
        self.scopes = {"class": None, "subroutine": None}

    def start_subroutine(self) -> None:
        self.scopes["subroutine"] = None
        self.i["arg"] = 0
        self.i["var"] = 0

    def define(self, name: str, type: str, kind: str) -> None: 
        if kind in ("static", "field"):
            scope = "class"
        elif kind in ("arg", "var"):
            scope = "subroutine"
        else:
            pass # is this needed?

        if self.scopes[scope] is None:
            self.scopes[scope] = {name: {"type": type, "kind": kind, "index": self.i[kind]}}
        else:
            self.scopes[scope][name] = {"type": type, "kind": kind, "index": self.i[kind]}

        self.i[kind] += 1

    def var_count(self, kind: str) -> None:
        return self.i[kind]

    def kind_of(self, scope: str, name: str) -> None:
        return self.scopes[scope][name]["kind"]

    def type_of(self, scope: str, name: str) -> None:
        return self.scopes[scope][name]["type"]

    def index_of(self, scope: str, name: str) -> None:
        return self.scopes[scope][name]["index"]
