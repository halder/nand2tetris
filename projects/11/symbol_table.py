class SymbolTable:
    # class scope: static, field
    # subroutine scope: arg, var

    def __init__(self) -> None:
        self.i = {"static": 0, "field": 0, "argument": 0, "local": 0}
        self.scopes = {"class": {}, "subroutine": {}}

    def start_subroutine(self) -> None:
        self.scopes["subroutine"] = {}
        self.i["argument"] = 0
        self.i["local"] = 0

    def define(self, name: str, type: str, kind: str) -> None: 
        if kind in ("static", "field"):
            scope = "class"
        elif kind in ("argument", "local"):
            scope = "subroutine"
    
        self.scopes[scope][name] = {"type": type, "kind": kind, "index": self.i[kind]}

        self.i[kind] += 1

    def var_count(self, kind: str) -> None:
        return self.i[kind]

    def kind_of(self, scope: str, name: str) -> None:
        kind = self.scopes[scope][name]["kind"]
        return kind if kind != "field" else "this"

    def type_of(self, scope: str, name: str) -> None:
        return self.scopes[scope][name]["type"]

    def index_of(self, scope: str, name: str) -> None:
        return self.scopes[scope][name]["index"]
