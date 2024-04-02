KEYWORDS = [
    "class", "constructor", "function", "method", "field", "static", "var",
    "int", "char", "boolean", "void", "true", "false", "null", "this", "let",
    "do", "if", "else", "while", "return"
]
SYMBOLS = "{}()[].,;+-*/&|<>=~"

def get_tokens(source_file: list[str]) -> list[dict]:
    list_of_tokens = []
    comment = False

    for line in source_file:
        # remove inline comments
        line = line.lstrip().split("//")[0]

        if "/*" in line and "*/" in line:
            continue
        elif "/*" in line:
            comment = True
            line = line.split("/*")[0]
        elif "*/" in line:
            comment = False
            line = line.split("*/")[1]

        if comment:
            continue
        
        if line:
            line_tokens = get_line_tokens(line)

            for token in line_tokens:
                list_of_tokens.append(token)

    typed_list_of_tokens = get_token_type(list_of_tokens)
        
    return typed_list_of_tokens


def get_line_tokens(line: str) -> list[dict]:
    line_tokens = []
    current_token = ""
    within_string = False

    for char in line:
        # beginning of string constant
        if char == '"' and not within_string:
            within_string = True
            continue

        if within_string:
            if char == '"':
                if current_token:
                    line_tokens.append({"type": "stringConstant", "value": current_token})
                current_token = ""
                within_string = False
                continue
            
        # whitespace outside of string constant
        if char in (" ", "\t") and not within_string:
            if current_token:
                line_tokens.append({"type": "other", "value": current_token})
            current_token = ""
            continue

        if char in SYMBOLS:
            if current_token:
                line_tokens.append({"type": "other", "value": current_token})

            line_tokens.append({"type": "symbol", "value": char})
            current_token = ""
            continue
        
        current_token = f"{current_token}{char}"

    return line_tokens


def get_token_type(list_of_tokens: list[dict]) -> list[dict]:
    typed_tokens = []

    for token in list_of_tokens:
        token_type, token_value = token["type"], token["value"]

        if not token_type == "other":
            typed_tokens.append(token)
        else:
            if token_value in KEYWORDS:
                typed_tokens.append({"type": "keyword", "value": token_value})

            elif token_value.isdigit():
                typed_tokens.append({"type": "integerConstant", "value": int(token_value)})
            
            else:
                typed_tokens.append({"type": "identifier", "value": token_value})

    return typed_tokens


if __name__ == "__main__":
    with open("Square/Main.jack", "r") as file:
        content = file.readlines()

    list_of_tokens = get_tokens(content)

    print(list_of_tokens)