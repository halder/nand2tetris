BIN_OPS = "+-*/&|<>="
OPS_MAP = {
        "binary": {
            "hack": {
                "+": "add",
                "-": "sub",
                "&": "and",
                "|": "or",
                "<": "lt",
                ">": "gt",
                "=": "eq"
            },
            "os": {
                "*": "Math.multiply",
                "/": "Math.divide"
            }
        },
        "unary": {
            "-": "neg",
            "~": "not"
        }
    }

def order_expression(expression: list) -> None:
    """Inplace postfix ordering of expression."""
    switch_i = []

    for i, term in enumerate(expression):
        if isinstance(term, list):
            order_expression(term)
        
        if str(term) in BIN_OPS:
            switch_i.append((i, len(expression) - 1))
        
    for pair in switch_i:
        i, j = pair
        expression[i], expression[j] = expression[j], expression[i]
