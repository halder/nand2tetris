"""
See jack_grammar.pdf for full grammar flow specification.

Optimizations:
    * compilation functions are very long, this can be (but probably never will be) optimized
    * current error handling extremely verbose 
    * lots of branching which could be reduced significantly
"""

from io import TextIOWrapper

class ParserError(Exception):
    def __init__(self, message):
        self.message = message


class Parser:
    def __init__(self, tokens: list[dict], file: TextIOWrapper) -> None:
        self.tokens = tokens
        self.n = len(self.tokens)
        self.i = 0
        self.current_type = self.tokens[self.i]["type"]
        self.current_value = self.tokens[self.i]["value"]
        self.file = file

    def has_more_tokens(self) -> bool:
        return True if (self.i + 1) < self.n else False
    
    def advance(self) -> None:
        self.write_terminal()

        if self.has_more_tokens():
            self.i += 1
            self.current_type = self.tokens[self.i]["type"]
            self.current_value = self.tokens[self.i]["value"]

    def write_terminal(self) -> None:
        symbol_map = {"<": "&lt;", ">": "&gt;", '"': "&quot;", "&": "&amp;"}
        
        current_value = self.current_value
        if current_value in symbol_map:
            current_value = symbol_map[current_value]

        self.file.write(f"<{self.current_type}> {current_value} </{self.current_type}>\n")
    
    def write_non_terminal(self, non_terminal: str, begin: bool = False) -> None:
        if begin:
            self.file.write(f"<{non_terminal}>\n")
        else:
            self.file.write(f"</{non_terminal}>\n")

    def peek(self) -> tuple[str]:
        if self.has_more_tokens():
            return self.tokens[self.i + 1]["type"], self.tokens[self.i + 1]["value"]

    def is_literal(self, next_type, next_value, expectation) -> bool:
        return next_type == "symbol" and next_value == expectation
    
    def is_type(self, next_type, next_value) -> bool:
        return self.is_identifier(next_type) or (self.is_keyword(next_type) and next_value in ("int", "char", "boolean"))
    
    def is_operation(self, next_type, next_value) -> bool:
        return next_type == "symbol" and next_value in "+-*/&|<>="
    
    def is_keyword(self, next_type) -> bool:
        return next_type == "keyword"

    def is_identifier(self, next_type) -> bool:
        return next_type == "identifier"
    
    def is_class_var_dec(self, next_type, next_value) -> bool:
        return self.is_keyword(next_type) and next_value in ("static", "field")
    
    def is_subroutine_dec(self, next_type, next_value) -> bool:
        return self.is_keyword(next_type) and next_value in ("constructor", "function", "method")

    def is_var_dec(self, next_type, next_value) -> bool:
        return self.is_keyword(next_type) and next_value == "var"
    
    def is_statement(self, next_type, next_value) -> bool:
        return self.is_keyword(next_type) and next_value in ("let", "if", "while", "do", "return")
    
    def is_expression(self, next_type, next_value) -> bool:
        return self.is_term(next_type, next_value)

    def is_expression_list(self, next_type, next_value) -> bool:
        return self.is_expression(next_type, next_value)

    def is_term(self, next_type, next_value) -> bool:
        return (
            self.is_identifier(next_type)
            or self.is_literal(next_type, next_value, "(")
            or self.is_literal(next_type, next_value, "-")
            or self.is_literal(next_type, next_value, "~")
            or self.is_keyword(next_type)
            or next_type == "integerConstant"
            or next_type == "stringConstant"
        )

    def compile(self) -> None:
        self.compile_class()
        print("Finished compilation.")

    def compile_class(self) -> None:
        if self.current_type != "keyword" and self.current_value != "class":
            raise ParserError(f"Jack program must start with 'class' keyword, found '{self.current_value}'")
        
        self.write_non_terminal("class", begin=True)

        next_type, next_value = self.peek()
        if self.is_identifier(next_type):
            self.advance()
        else:
            raise ParserError(f"expected identifier after 'class', found '{next_type}': '{next_value}'")

        next_type, next_value = self.peek()
        if self.is_literal(next_type, next_value, "{"):
            self.advance()
        else:
            raise ParserError(f"expected '{{' after identifier, found '{next_type}': '{next_value}'")

        next_type, next_value = self.peek()
        if self.is_class_var_dec(next_type, next_value):
            self.advance()
            while self.is_class_var_dec(self.current_type, self.current_value):
                self.compile_class_var_dec()
        
            while self.is_subroutine_dec(self.current_type, self.current_value):
                self.compile_subroutine()

        elif self.is_subroutine_dec(next_type, next_value):
            self.advance()

            while self.is_subroutine_dec(self.current_type, self.current_value):
                self.compile_subroutine()
            
        elif self.is_literal(next_type, next_value, "}"):
            self.advance()

        else:
            raise ParserError(f"expected classVarDec or '}}' after '{{', found '{next_type}': '{next_value}'")
        
        self.advance() # final '}'
        
        self.write_non_terminal("class")

    def compile_class_var_dec(self) -> None:
        self.write_non_terminal("classVarDec", begin=True)

        next_type, next_value = self.peek()
        if self.is_type(next_type, next_value):
            self.advance()
        else:
            raise ParserError(f"expected 'int', 'char', 'boolean' or identifier after '{self.current_value}', found '{next_type}': '{next_value}'")
        
        next_type, next_value = self.peek()
        if self.is_identifier(next_type):
            self.advance()
        else:
            raise ParserError(f"expected identifier after '{self.current_type}': '{self.current_value}', found '{next_type}': '{next_value}'")
        
        next_type, next_value = self.peek()
        while self.is_literal(next_type, next_value, ","):
            self.advance()

            next_type, next_value = self.peek()
            if self.is_identifier(next_type):
                self.advance()
            else:
                raise ParserError(f"expected identifier after ',', found '{next_type}': '{next_value}'")

            next_type, next_value = self.peek()

        if self.is_literal(next_type, next_value, ";"):
            self.advance()
        else:
            raise ParserError(f"expected ';' or ',' after identifier, found '{next_type}': '{next_value}'")

        next_type, next_value = self.peek()
        if self.is_literal(next_type, next_value, "}") or self.is_class_var_dec(next_type, next_value) or self.is_subroutine_dec(next_type, next_value):
            self.advance()
        else:
            raise ParserError(f"classVarDec must be followed by '}}' or subroutineDec, found '{next_type}': '{next_value}'")

        self.write_non_terminal("classVarDec")

    def compile_subroutine(self) -> None:
        self.write_non_terminal("subroutineDec", begin=True)

        next_type, next_value = self.peek()
        if self.is_type(next_type, next_value) or (self.is_keyword(next_type) and next_value == "void"):
            self.advance()
        else:
            raise ParserError(f"expected 'void', 'int', 'char', 'boolean' or identifier after {self.current_value}, found '{next_type}': '{next_value}'")
        
        next_type, next_value = self.peek()
        if self.is_identifier(next_type):
            self.advance()
        else:
            raise ParserError(f"expected identifier after '{self.current_type}': '{self.current_value}', found '{next_type}': '{next_value}'")
        
        next_type, next_value = self.peek()
        if self.is_literal(next_type, next_value, "("):
            self.advance()
        else:
            raise ParserError(f"expected '(' after identifier, found '{next_type}': '{next_value}'")
        
        next_type, next_value = self.peek()
        if self.is_type(next_type, next_value):
            self.advance()
            self.compile_parameter_list()
        elif self.is_literal(next_type, next_value, ")"):
            self.advance()
            self.write_non_terminal("parameterList", begin=True)
            self.write_non_terminal("parameterList")
        else:
            raise ParserError(f"expected ')' or parameterList after '(', found '{next_type}': '{next_value}'")

        next_type, next_value = self.peek()
        if self.is_literal(next_type, next_value, "{"):
            self.advance()
        else:
            raise ParserError(f"expected '{{' after '(', found '{next_type}': '{next_value}'")

        self.write_non_terminal("subroutineBody", begin=True)

        next_type, next_value = self.peek()
        if self.is_var_dec(next_type, next_value):
            self.advance()
            while self.is_var_dec(self.current_type, self.current_value):
                self.compile_var_dec()
                
            while self.is_statement(self.current_type, self.current_value):
                self.compile_statements()

        elif self.is_statement(next_type, next_value):
            self.advance()

            while self.is_statement(self.current_type, self.current_value):
                self.compile_statements()

        elif self.is_literal(next_type, next_value, "}"):
            self.advance()
            self.write_non_terminal("statements", begin=True)
            self.write_non_terminal("statements")

        else:
            raise ParserError(f"expected varDec or '}}' after '{{', found '{next_type}': '{next_value}'")
        
        next_type, next_value = self.peek()
        if self.is_subroutine_dec(next_type, next_value) or self.is_literal(next_type, next_value, "}"):
            self.advance()
        else:
            raise ParserError(f"subroutineDec must be followed by subroutineDec or '}}', found '{next_type}': '{next_value}'")

        self.write_non_terminal("subroutineBody")
        self.write_non_terminal("subroutineDec")

    def compile_parameter_list(self) -> None:
        self.write_non_terminal("parameterList", begin=True)

        next_type, next_value = self.peek()
        if self.is_identifier(next_type):
            self.advance()
        else:
            raise ParserError(f"expected identifier after '{self.current_value}', found '{next_type}': '{next_value}'")

        next_type, next_value = self.peek()
        while self.is_literal(next_type, next_value, ","):
            self.advance()

            next_type, next_value = self.peek()
            if self.is_type(next_type, next_value):
                self.advance()
            else:
                raise ParserError(f"expected type after ',', found '{next_type}': '{next_value}'")
            
            next_type, next_value = self.peek()
            if self.is_identifier(next_type):
                self.advance()
            else:
                raise ParserError(f"expected identifier after '{self.current_value}', found '{next_type}': '{next_value}'")
            
            next_type, next_value = self.peek()
        
        if self.is_literal(next_type, next_value, ")"):
            self.advance()
        else:
            raise ParserError(f"parameterList must be followed by ')', found '{next_type}': '{next_value}'")

        self.write_non_terminal("parameterList")

    def compile_var_dec(self) -> None:
        self.write_non_terminal("varDec", begin=True)

        next_type, next_value = self.peek()
        if self.is_type(next_type, next_value):
            self.advance()
        else:
            raise ParserError(f"expected type after 'var', found '{next_type}': '{next_value}'")
        
        next_type, next_value = self.peek()
        if self.is_identifier(next_type):
            self.advance()
        else:
            raise ParserError(f"expected identifier after '{self.current_value}', found '{next_type}': '{next_value}'")

        next_type, next_value = self.peek()
        while self.is_literal(next_type, next_value, ","):
            self.advance()
            next_type, next_value = self.peek()
            if self.is_identifier(next_type):
                self.advance()
            else:
                raise ParserError(f"expected identifier after ',', found '{next_type}': '{next_value}'")

            next_type, next_value = self.peek()

        if self.is_literal(next_type, next_value, ";"):
            self.advance()
        else:
            raise ParserError(f"expected ';' or ',' after identifier, found '{next_type}': '{next_value}'")

        next_type, next_value = self.peek()
        if self.is_literal(next_type, next_value, "}") or self.is_var_dec(next_type, next_value) or self.is_statement(next_type, next_value):
            self.advance()

        self.write_non_terminal("varDec")

    def compile_statements(self) -> None:
        self.write_non_terminal("statements", begin=True)

        while self.is_statement(self.current_type, self.current_value):

            if self.current_value == "let":
                self.compile_let()
                
            elif self.current_value == "if":
                self.compile_if()
                
            elif self.current_value == "while":
                self.compile_while()
                
            elif self.current_value == "do":
                self.compile_do()

            else: # "return"
                self.compile_return()

        self.write_non_terminal("statements")

    def compile_do(self) -> None:
        self.write_non_terminal("doStatement", begin=True)

        next_type, next_value = self.peek()
        if self.is_identifier(next_type):
            self.advance()
        else:
            raise ParserError(f"expected identifier after 'do' in do statement, found '{next_type}': '{next_value}'")

        next_type, next_value = self.peek()
        if self.is_literal(next_type, next_value, "."):
            self.advance()

            next_type, next_value = self.peek()
            if self.is_identifier(next_type):
                self.advance()
            else:
                raise ParserError(f"expected identifier after '.' in do statement, found '{next_type}': '{next_value}'")

            next_type, next_value = self.peek()
            if self.is_literal(next_type, next_value, "("):
                self.advance()
            else:
                raise ParserError(f"expected '(' after identifier in method/function call do statement, found '{next_type}': '{next_value}'")
            
        elif self.is_literal(next_type, next_value, "("):
            self.advance()
        else:
            raise ParserError(f"expected '(' or '.' after initial identifier in do statement, found '{next_type}': '{next_value}'")

        next_type, next_value = self.peek()
        if self.is_expression(next_type, next_value):
            self.advance()
            self.compile_expression_list()
        elif self.is_literal(next_type, next_value, ")"):
            self.advance()
            self.write_non_terminal("expressionList", begin=True)
            self.write_non_terminal("expressionList")
        else:
            raise ParserError(f"expected expessionList or ')' after '(' in do statement, found '{next_type}': '{next_value}'")

        next_type, next_value = self.peek()
        if self.is_literal(next_type, next_value, ";"):
            self.advance()
        else:
            raise ParserError(f"do statement must end with ';', found '{next_type}': '{next_value}'")

        next_type, next_value = self.peek()
        if self.is_statement(next_type, next_value) or self.is_literal(next_type, next_value, "}"):
            self.advance()
        else:
            raise ParserError(f"'do' statement must be followed by another statement or '}}', found '{next_type}': '{next_value}'")

        self.write_non_terminal("doStatement")

    def compile_let(self) -> None:
        self.write_non_terminal("letStatement", begin=True)

        next_type, next_value = self.peek()
        if self.is_identifier(next_type):
            self.advance()
        else:
            raise ParserError(f"expected identifier after 'let' in let statement, found '{next_type}': '{next_value}'")

        next_type, next_value = self.peek()
        if self.is_literal(next_type, next_value, "["):
            self.advance()

            next_type, next_value = self.peek()
            if self.is_expression(next_type, next_value):
                self.advance()
                self.compile_expression()
            
            if not self.is_literal(self.current_type, self.current_value, "]"):
                raise ParserError(f"expected ']' after expression within 'let' statement, found '{self.current_type}', '{self.current_value}'")

            next_type, next_value = self.peek()
            if self.is_literal(next_type, next_value, "="):
                self.advance()
            else:
                raise ParserError(f"expected '=' after ']', found '{next_type}': '{next_value}'")
        
        elif self.is_literal(next_type, next_value, "="):
            self.advance()
        else:
            raise ParserError(f"expected '=' or '[' after identifier, found '{next_type}': '{next_value}'")
        
        next_type, next_value = self.peek()
        if self.is_expression(next_type, next_value):
            self.advance()
            self.compile_expression()

        if not self.is_literal(self.current_type, self.current_value, ";"):
            raise ParserError(f"'let' statement must end with ';', found '{self.current_type}': '{self.current_value}'")

        next_type, next_value = self.peek()
        if self.is_statement(next_type, next_value) or self.is_literal(next_type, next_value, "}"):
            self.advance()
        else:
            raise ParserError(f"'let' statement must be followed by another statement or '}}', found '{next_type}': '{next_value}'")

        self.write_non_terminal("letStatement")

    def compile_while(self) -> None:
        self.write_non_terminal("whileStatement", begin=True)

        next_type, next_value = self.peek()
        if self.is_literal(next_type, next_value, "("):
            self.advance()
        else:
            raise ParserError(f"expected '(' after 'while' in while statement, found '{next_type}': '{next_value}'")

        next_type, next_value = self.peek()
        if self.is_expression(next_type, next_value):
            self.advance()
        else:
            raise ParserError(f"expected expression after '(' in while statement, found '{next_type}': '{next_value}'")
    
        self.compile_expression()

        if not self.is_literal(self.current_type, self.current_value, ")"):
            raise ParserError(f"expected ')' after expression within 'while' statement, found '{self.current_type}', '{self.current_value}'")

        next_type, next_value = self.peek()
        if self.is_literal(next_type, next_value, "{"):
            self.advance()
        else:
            raise ParserError(f"expected '{{' after ')' in 'while' statement, found '{next_type}': '{next_value}'")

        next_type, next_value = self.peek()
        if self.is_statement(next_type, next_value):
            self.advance()
            self.compile_statements()
        elif self.is_literal(next_type, next_value, "}"):
            self.advance()
            self.write_non_terminal("statements", begin=True)
            self.write_non_terminal("statements")
        else:
            raise ParserError(f"expected statement(s) or '}}' after '{{' in 'if' statement, found '{next_type}': '{next_value}'")

        next_type, next_value = self.peek()
        if self.is_statement(next_type, next_value) or self.is_literal(next_type, next_value, "}"):
            self.advance()
        else:
            raise ParserError(f"'while' statement must be followed by another statement or '}}', found '{next_type}': '{next_value}'")

        self.write_non_terminal("whileStatement")

    def compile_return(self) -> None:
        self.write_non_terminal("returnStatement", begin=True)

        next_type, next_value = self.peek()
        if self.is_expression(next_type, next_value):
            self.advance()
            self.compile_expression()
        elif self.is_literal(next_type, next_value, ";"):
            self.advance()
        else:
            raise ParserError(f"expected expression or ';' after 'return' in return statement, found '{next_type}': '{next_value}'")

        next_type, next_value = self.peek()
        if self.is_statement(next_type, next_value) or self.is_literal(next_type, next_value, "}"):
            self.advance()
        else:
            raise ParserError(f"'return' statement must be followed by another statement or '}}', found '{next_type}': '{next_value}'")

        self.write_non_terminal("returnStatement")

    def compile_if(self) -> None:
        self.write_non_terminal("ifStatement", begin=True)

        next_type, next_value = self.peek()
        if self.is_literal(next_type, next_value, "("):
            self.advance()
        else:
            raise ParserError(f"expected '(' after 'if', found '{next_type}': '{next_value}'")

        next_type, next_value = self.peek()
        if self.is_expression(next_type, next_value):
            self.advance()
        else:
            raise ParserError(f"expected expression after '(' in 'if' statement, found '{next_type}': '{next_value}'")

        self.compile_expression()

        if not self.is_literal(self.current_type, self.current_value, ")"):
            raise ParserError(f"expected ')' after expression within 'if' statement, found '{self.current_type}', '{self.current_value}'")

        next_type, next_value = self.peek()
        if self.is_literal(next_type, next_value, "{"):
            self.advance()
        else:
            raise ParserError(f"expected '{{' after ')' in 'if' statement, found '{next_type}': '{next_value}'")

        next_type, next_value = self.peek()
        if self.is_statement(next_type, next_value):
            self.advance()
            self.compile_statements()
        elif self.is_literal(next_type, next_value, "}"):
            self.advance()
            self.write_non_terminal("statements", begin=True)
            self.write_non_terminal("statements")
        else:
            raise ParserError(f"expected statement(s) or '}}' after '{{' in 'if' statement, found '{next_type}': '{next_value}'")

        next_type, next_value = self.peek()
        if self.is_keyword(next_type) and next_value == "else":
            self.advance()
            
            next_type, next_value = self.peek()
            if self.is_literal(next_type, next_value, "{"):
                self.advance()
            else:
                raise ParserError(f"expected '{{' after 'else' in else clause, found '{next_type}': '{next_value}'")

            next_type, next_value = self.peek()
            if self.is_statement(next_type, next_value):
                self.advance()
                self.compile_statements()
            elif self.is_literal(next_type, next_value, "}"):
                self.advance()
                self.write_non_terminal("statements", begin=True)
                self.write_non_terminal("statements")
            else:
                raise ParserError(f"expected statement(s) or '}}' after '{{' in else clause in 'if' statement, found '{next_type}': '{next_value}'")

        next_type, next_value = self.peek()
        if self.is_statement(next_type, next_value) or self.is_literal(next_type, next_value, "}"):
            self.advance()
        else:
            raise ParserError(f"'if' statement must be followed by another statement or '}}', found '{next_type}': '{next_value}'")

        self.write_non_terminal("ifStatement")

    def compile_expression_list(self) -> None:
        self.write_non_terminal("expressionList", begin=True)
        
        self.compile_expression()

        while self.is_literal(self.current_type, self.current_value, ","):
            next_type, next_value = self.peek()
            if self.is_expression(next_type, next_value):
                self.advance()
                self.compile_expression()
            else:
                raise ParserError(f"expected expression after ',' in expressionList, found '{next_type}': '{next_value}'")

        if not self.is_literal(self.current_type, self.current_value, ")"):
            raise ParserError(f"expressionList must close with ')', found '{next_type}': '{next_value}'")

        self.write_non_terminal("expressionList")

    def compile_expression(self) -> None:
        self.write_non_terminal("expression", begin=True)

        self.compile_term()

        while self.is_operation(self.current_type, self.current_value):
            next_type, next_value = self.peek()
            if self.is_term(next_type, next_value):
                self.advance()
                self.compile_term()
            else:
                raise ParserError(f"expected term after '{self.current_value}' in expression, found '{next_type}': '{next_value}'")
                
        if not (
            self.is_literal(self.current_type, self.current_value, ",")
            or self.is_literal(self.current_type, self.current_value, ";")
            or self.is_literal(self.current_type, self.current_value, "]")
            or self.is_literal(self.current_type, self.current_value, ")")
        ):
            raise ParserError(f"expression must be followed by ',', ';', ']' or ')', found '{self.current_type}': '{self.current_value}'")

        self.write_non_terminal("expression")

    def compile_term(self) -> None:
        self.write_non_terminal("term", begin=True)

        if self.is_keyword(self.current_type) or self.current_type == "integerConstant" or self.current_type == "stringConstant":
            self.advance()
        
        elif self.is_literal(self.current_type, self.current_value, "-") or self.is_literal(self.current_type, self.current_value, "~"):
            next_type, next_value = self.peek()
            if self.is_term(next_type, next_value):
                self.advance()
                self.compile_term()
            else:
                raise ParserError(f"expected term after '{self.current_value}' in term, found '{next_type}': '{next_value}'")

        elif self.is_literal(self.current_type, self.current_value, "("):
            next_type, next_value = self.peek()
            if self.is_expression(next_type, next_value):
                self.advance()
                self.compile_expression()
            else:
                raise ParserError(f"expected expression after '(' in term, found '{next_type}': '{next_value}'")

            if not self.is_literal(self.current_type, self.current_value, ")"):
                raise ParserError(f"expected ')' after expression in term, found '{next_type}': '{next_value}'")
            
            self.advance()

        elif self.is_identifier(self.current_type):
            next_type, next_value = self.peek()
            
            if self.is_literal(next_type, next_value, "."):
                self.advance()

                next_type, next_value = self.peek()
                if self.is_identifier(next_type):
                    self.advance()
                else:
                    raise ParserError(f"expected identifier after '.' in subroutine call within term, found '{next_type}': '{next_value}'")

                next_type, next_value = self.peek()
                if self.is_literal(next_type, next_value, "("):
                    self.advance()
                else:
                    raise ParserError(f"expected '(' after identifier in subroutine call within term, found '{next_type}': '{next_value}'")
                
                next_type, next_value = self.peek()
                if self.is_expression(next_type, next_value):
                    self.advance()
                    self.compile_expression_list()        
                elif self.is_literal(next_type, next_value, ")"):
                    self.advance()
                    self.write_non_terminal("expressionList", begin=True)
                    self.write_non_terminal("expressionList")
                else:
                    raise ParserError(f"expected expressionList or ')' after '(' in function call within term, found '{next_type}': '{next_value}'")

            elif self.is_literal(next_type, next_value, "("):
                self.advance()

                next_type, next_value = self.peek()
                if self.is_expression(next_type, next_value):
                    self.advance()
                    self.compile_expression_list()        
                elif self.is_literal(next_type, next_value, ")"):
                    self.advance()
                    self.write_non_terminal("expressionList", begin=True)
                    self.write_non_terminal("expressionList")
                else:
                    raise ParserError(f"expected expressionList or ')' after '(' in method call within term, found '{next_type}': '{next_value}'")

            elif self.is_literal(next_type, next_value, "["):
                self.advance()

                next_type, next_value = self.peek()
                if self.is_expression(next_type, next_value):
                    self.advance()
                    self.compile_expression()
                else:
                    raise ParserError(f"expected expression after '[' in array indexing within term, found '{next_type}': '{next_value}'")

            self.advance()
            
        else:
            raise ParserError(f"illegal term begin, found '{next_type}': '{next_value}'")

        if not (
            self.is_operation(self.current_type, self.current_value)
            or self.is_literal(self.current_type, self.current_value, ",")
            or self.is_literal(self.current_type, self.current_value, ";")
            or self.is_literal(self.current_type, self.current_value, ")")
            or self.is_literal(self.current_type, self.current_value, "]")
        ):
            raise ParserError(f"term must be followed by operation, ',', ';', ']' or ')', found '{self.current_type}': '{self.current_value}'")

        self.write_non_terminal("term")