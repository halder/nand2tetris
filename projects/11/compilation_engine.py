"""
See documents/jack_grammar.pdf for full grammar flow specification.
"""

from io import TextIOWrapper

import symbol_table
import vm_writer
import util

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
        self.symbol_table = symbol_table.SymbolTable()
        self.vm_writer = vm_writer.VMWriter(file)
        self.label_counter = 0

    def code_write(self, expression: list) -> None:
        if isinstance(expression, int):
            self.vm_writer.write_push("constant", expression)
        
        elif isinstance(expression, str):
            if expression == "true":
                self.vm_writer.write_push("constant", 1)
                self.vm_writer.write_arithmetic("neg")
            elif expression == "false" or expression == "null":
                self.vm_writer.write_push("constant", 0)
            elif expression == "this":
                self.vm_writer.write_push("pointer", 0)
            elif expression.startswith("__STR_CONST__$"):
                expression = expression[expression.index("$")+1:]
                self.vm_writer.write_push("constant", len(expression))
                self.vm_writer.write_call("String.new", 1)

                for char in expression:
                    self.vm_writer.write_push("constant", ord(char))
                    self.vm_writer.write_call("String.appendChar", 2)

            elif expression in self.symbol_table.scopes["subroutine"]:
                scope = "subroutine"
                self.vm_writer.write_push(self.symbol_table.kind_of(scope, expression), self.symbol_table.index_of(scope, expression))
            elif expression in self.symbol_table.scopes["class"]:
                scope = "class"
                self.vm_writer.write_push(self.symbol_table.kind_of(scope, expression), self.symbol_table.index_of(scope, expression))
            else:
                # some kind of empty function call
                if "." in expression:
                    object, function = expression.split(".")

                    # `do object.some_method()`
                    if object in self.symbol_table.scopes["class"]:
                        self.vm_writer.write_push(self.symbol_table.kind_of("class", object), self.symbol_table.index_of("class", object))
                        self.vm_writer.write_call(f"{self.symbol_table.type_of('class', object)}.{function}", 1)
 
                    elif object in self.symbol_table.scopes["subroutine"]:
                        self.vm_writer.write_push(self.symbol_table.kind_of("subroutine", object), self.symbol_table.index_of("subroutine", object))
                        self.vm_writer.write_call(f"{self.symbol_table.type_of('subroutine', object)}.{function}", 1)
 
                    else: # function call e.g. `do SomeClass.some_function()`
                        self.vm_writer.write_call(expression, 0)
                else:
                    # method call within class e.g. `do some_method()`
                    self.vm_writer.write_call(expression, 0)

        elif isinstance(expression, list) and len(expression) == 1:
            if isinstance(expression[0], dict):
                self.vm_writer.write_push("pointer", 0)
                self.vm_writer.write_call(expression[0]["class_method"], 1)
            else:
                self.code_write(expression[0])
        
        elif isinstance(expression, list) and len(expression) == 2:
            if any([isinstance(expr, dict) for expr in expression]):
                if "array" in expression[0]:
                    self.code_write(expression[0]["array"])
                    self.code_write(expression[1]) # index expression
                    self.vm_writer.write_arithmetic("add")
                    self.vm_writer.write_pop("pointer", 1)
                    self.vm_writer.write_push("that", 0)
                
                elif "class_method" in expression[0]:
                    self.vm_writer.write_push("pointer", 0)
                    self.code_write(expression[1])
                    self.vm_writer.write_call(expression[0]["class_method"], 1+len(expression[1]))

            elif "~" in expression or "-" in expression:
                if expression[1] == "~" or expression[1] == "-":
                    expression[0], expression[1] = expression[1], expression[0]
                
                self.code_write(expression[1])
                self.vm_writer.write_arithmetic(util.OPS_MAP["unary"][expression[0]])

            elif any([isinstance(expr, str) for expr in expression]):
                # function call
                if isinstance(expression[1], str):
                    expression[0], expression[1] = expression[1], expression[0]
                
                self.code_write(expression[1]) # push arguments
                if "." in expression[0]:
                    object, function = expression[0].split(".")

                    if object in self.symbol_table.scopes["class"]:
                        self.vm_writer.write_push(self.symbol_table.kind_of("class", object), self.symbol_table.index_of("class", object))
                        self.vm_writer.write_call(f"{self.symbol_table.type_of('class', object)}.{function}", 1+len(expression[1]))
 
                    elif object in self.symbol_table.scopes["subroutine"]:
                        self.vm_writer.write_push(self.symbol_table.kind_of("subroutine", object), self.symbol_table.index_of("subroutine", object))
                        self.vm_writer.write_call(f"{self.symbol_table.type_of('subroutine', object)}.{function}", 1+len(expression[1]))
 
                    else: # function call e.g. `do SomeClass.some_function()`
                        self.vm_writer.write_call(expression[0], len(expression[1]))

                else:
                    self.vm_writer.write_call(expression[0], len(expression[1]))

            else:
                self.code_write(expression[0])
                self.code_write(expression[1])
        
        elif (isinstance(expression, list) and len(expression) == 3) and isinstance(expression[2], str):
            self.code_write(expression[0])
            self.code_write(expression[1])

            if expression[2] in util.OPS_MAP["binary"]["hack"]:
                self.vm_writer.write_arithmetic(util.OPS_MAP["binary"]["hack"][expression[2]])
            else: # Math module operation
                self.vm_writer.write_call(util.OPS_MAP["binary"]["os"][expression[2]], 2)
        
        else:
            for expr in expression:
                self.code_write(expr)

    def generate_labels(self, statement: str) -> list[str]:
            """
            statement: "while"  -> [label_while_end, label_while_expression]
            statement: "if"     -> [if_end_label, if_false_label]
            """
            labels = []
            if statement == "while":
                labels.append(f"{self.current_class}.{self.current_subroutine}__{statement.upper()}_END${self.label_counter}")
                labels.append(f"{self.current_class}.{self.current_subroutine}__{statement.upper()}_EXPR${self.label_counter}")
                
                self.label_counter += 1
            
            elif statement == "if":
                labels.append(f"{self.current_class}.{self.current_subroutine}__{statement.upper()}_END${self.label_counter}")
                labels.append(f"{self.current_class}.{self.current_subroutine}__{statement.upper()}_FALSE${self.label_counter}")
                
                self.label_counter += 1
            
            else:
                raise ValueError("label must be either of 'while', 'if'.")

            return labels

    def has_more_tokens(self) -> bool:
        return True if (self.i + 1) < self.n else False
    
    def advance(self) -> None:
        if self.has_more_tokens():
            self.i += 1
            self.current_type = self.tokens[self.i]["type"]
            self.current_value = self.tokens[self.i]["value"]

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

    def compile_class(self) -> None:
        if self.current_type != "keyword" and self.current_value != "class":
            raise ParserError(f"Jack program must start with 'class' keyword, found '{self.current_value}'")

        next_type, next_value = self.peek()
        if self.is_identifier(next_type):
            self.advance()
            self.current_class = self.current_value
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
        
    def compile_class_var_dec(self) -> None:
        var_kind = self.current_value
        
        next_type, next_value = self.peek()
        if self.is_type(next_type, next_value):
            self.advance()
            var_type = self.current_value
        else:
            raise ParserError(f"expected 'int', 'char', 'boolean' or identifier after '{self.current_value}', found '{next_type}': '{next_value}'")
        
        next_type, next_value = self.peek()
        if self.is_identifier(next_type):
            self.advance()
            var_name = self.current_value
        else:
            raise ParserError(f"expected identifier after '{self.current_type}': '{self.current_value}', found '{next_type}': '{next_value}'")
        
        self.symbol_table.define(var_name, var_type, var_kind)

        next_type, next_value = self.peek()
        while self.is_literal(next_type, next_value, ","):
            self.advance()

            next_type, next_value = self.peek()
            if self.is_identifier(next_type):
                self.advance()
                var_name = self.current_value
                self.symbol_table.define(var_name, var_type, var_kind)

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

    def compile_subroutine(self) -> None:
        self.symbol_table.start_subroutine()

        if self.current_value == "method":
            is_method = True
        else:
            is_method = False

        if self.current_value == "constructor":
            self.is_constructor = True
            n_class_fields = self.symbol_table.var_count("field")
        else:
            self.is_constructor = False

        next_type, next_value = self.peek()
        if self.is_type(next_type, next_value) or (self.is_keyword(next_type) and next_value == "void"):
            self.advance()
        else:
            raise ParserError(f"expected 'void', 'int', 'char', 'boolean' or identifier after {self.current_value}, found '{next_type}': '{next_value}'")
        
        next_type, next_value = self.peek()
        if self.is_identifier(next_type):
            self.advance()
            self.current_subroutine = self.current_value
            function_name = self.current_value
        else:
            raise ParserError(f"expected identifier after '{self.current_type}': '{self.current_value}', found '{next_type}': '{next_value}'")
        
        next_type, next_value = self.peek()
        if self.is_literal(next_type, next_value, "("):
            self.advance()
        else:
            raise ParserError(f"expected '(' after identifier, found '{next_type}': '{next_value}'")
        
        if is_method:
            self.symbol_table.define("this", self.current_class, "argument")

        next_type, next_value = self.peek()
        if self.is_type(next_type, next_value):
            self.advance()
            self.compile_parameter_list()
        elif self.is_literal(next_type, next_value, ")"):
            self.advance()
        else:
            raise ParserError(f"expected ')' or parameterList after '(', found '{next_type}': '{next_value}'")

        next_type, next_value = self.peek()
        if self.is_literal(next_type, next_value, "{"):
            self.advance()
        else:
            raise ParserError(f"expected '{{' after '(', found '{next_type}': '{next_value}'")

        n_args = 0

        next_type, next_value = self.peek()
        if self.is_var_dec(next_type, next_value):
            self.advance()
            while self.is_var_dec(self.current_type, self.current_value):
                n_args += self.compile_var_dec()
                
            self.vm_writer.write_function(f"{self.current_class}.{function_name}", n_args)

            if is_method:
                self.vm_writer.write_push("argument", 0)
                self.vm_writer.write_pop("pointer", 0)

            if self.is_constructor:
                self.vm_writer.write_push("constant", n_class_fields)
                self.vm_writer.write_call("Memory.alloc", 1)
                self.vm_writer.write_pop("pointer", 0)

            while self.is_statement(self.current_type, self.current_value):
                self.compile_statements()

        elif self.is_statement(next_type, next_value):
            self.advance()

            self.vm_writer.write_function(f"{self.current_class}.{function_name}", n_args)

            if is_method:
                self.vm_writer.write_push("argument", 0)
                self.vm_writer.write_pop("pointer", 0)

            if self.is_constructor:
                self.vm_writer.write_push("constant", n_class_fields)
                self.vm_writer.write_call("Memory.alloc", 1)
                self.vm_writer.write_pop("pointer", 0)

            while self.is_statement(self.current_type, self.current_value):
                self.compile_statements()

        elif self.is_literal(next_type, next_value, "}"):
            self.advance()
            self.vm_writer.write_function(f"{self.current_class}.{function_name}", n_args)

            if is_method:
                self.vm_writer.write_push("argument", 0)
                self.vm_writer.write_pop("pointer", 0)

            if self.is_constructor:
                self.vm_writer.write_push("constant", n_class_fields)
                self.vm_writer.write_call("Memory.alloc", 1)
                self.vm_writer.write_pop("pointer", 0)

        else:
            raise ParserError(f"expected varDec or '}}' after '{{', found '{next_type}': '{next_value}'")
        
        next_type, next_value = self.peek()
        if self.is_subroutine_dec(next_type, next_value) or self.is_literal(next_type, next_value, "}"):
            self.advance()
        else:
            raise ParserError(f"subroutineDec must be followed by subroutineDec or '}}', found '{next_type}': '{next_value}'")

    def compile_parameter_list(self) -> None:
        var_kind = "argument"
        var_type = self.current_value
        
        next_type, next_value = self.peek()
        if self.is_identifier(next_type):
            self.advance()

            var_name = self.current_value
            self.symbol_table.define(var_name, var_type, var_kind)
        else:
            raise ParserError(f"expected identifier after '{self.current_value}', found '{next_type}': '{next_value}'")

        next_type, next_value = self.peek()
        while self.is_literal(next_type, next_value, ","):
            self.advance()

            next_type, next_value = self.peek()
            if self.is_type(next_type, next_value):
                self.advance()

                var_type = self.current_value
            else:
                raise ParserError(f"expected type after ',', found '{next_type}': '{next_value}'")
            
            next_type, next_value = self.peek()
            if self.is_identifier(next_type):
                self.advance()

                var_name = self.current_value
                self.symbol_table.define(var_name, var_type, var_kind)
            else:
                raise ParserError(f"expected identifier after '{self.current_value}', found '{next_type}': '{next_value}'")
            
            next_type, next_value = self.peek()
        
        if self.is_literal(next_type, next_value, ")"):
            self.advance()
        else:
            raise ParserError(f"parameterList must be followed by ')', found '{next_type}': '{next_value}'")

    def compile_var_dec(self) -> int:
        n_args = 1
        var_kind = "local"

        next_type, next_value = self.peek()
        if self.is_type(next_type, next_value):
            self.advance()
            var_type = self.current_value
        else:
            raise ParserError(f"expected type after 'var', found '{next_type}': '{next_value}'")
        
        next_type, next_value = self.peek()
        if self.is_identifier(next_type):
            self.advance()

            var_name = self.current_value
            self.symbol_table.define(var_name, var_type, var_kind)
        else:
            raise ParserError(f"expected identifier after '{self.current_value}', found '{next_type}': '{next_value}'")

        next_type, next_value = self.peek()
        while self.is_literal(next_type, next_value, ","):
            self.advance()
            next_type, next_value = self.peek()

            if self.is_identifier(next_type):
                self.advance()

                var_name = self.current_value
                self.symbol_table.define(var_name, var_type, var_kind)
            else:
                raise ParserError(f"expected identifier after ',', found '{next_type}': '{next_value}'")

            n_args +=1 

            next_type, next_value = self.peek()

        if self.is_literal(next_type, next_value, ";"):
            self.advance()
        else:
            raise ParserError(f"expected ';' or ',' after identifier, found '{next_type}': '{next_value}'")

        next_type, next_value = self.peek()
        if self.is_literal(next_type, next_value, "}") or self.is_var_dec(next_type, next_value) or self.is_statement(next_type, next_value):
            self.advance()

        return n_args

    def compile_statements(self) -> None:
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

    def compile_do(self) -> None:
        n_args = 0

        next_type, next_value = self.peek()
        if self.is_identifier(next_type):
            self.advance()
            
            callee = self.current_value
            is_variable_method_call = False

            if callee in self.symbol_table.scopes["class"]:
                is_variable_method_call = True
                scope = "class"
                var_name = callee

            if callee in self.symbol_table.scopes["subroutine"]:
                is_variable_method_call = True
                scope = "subroutine"
                var_name = callee

        else:
            raise ParserError(f"expected identifier after 'do' in do statement, found '{next_type}': '{next_value}'")

        next_type, next_value = self.peek()
        if self.is_literal(next_type, next_value, "."):
            self.advance()

            next_type, next_value = self.peek()
            if self.is_identifier(next_type):
                self.advance()
                function_name = self.current_value
            else:
                raise ParserError(f"expected identifier after '.' in do statement, found '{next_type}': '{next_value}'")

            next_type, next_value = self.peek()
            if self.is_literal(next_type, next_value, "("):
                self.advance()
            else:
                raise ParserError(f"expected '(' after identifier in method/function call do statement, found '{next_type}': '{next_value}'")

            if is_variable_method_call:
                n_args += 1
                callee = self.symbol_table.type_of(scope, callee)
                self.vm_writer.write_push(self.symbol_table.kind_of(scope, var_name), self.symbol_table.index_of(scope, var_name))
        
        elif self.is_literal(next_type, next_value, "("):
            n_args += 1
            callee = self.current_class
            function_name = self.current_value
            self.vm_writer.write_push("pointer", 0)
            
            self.advance()
        else:
            raise ParserError(f"expected '(' or '.' after initial identifier in do statement, found '{next_type}': '{next_value}'")

        next_type, next_value = self.peek()
        if self.is_expression(next_type, next_value):
            self.advance()

            n_args_params, expression_list = self.compile_expression_list()
            n_args += n_args_params
            for expression in expression_list:
                util.order_expression(expression)
                self.code_write(expression)

        elif self.is_literal(next_type, next_value, ")"):
            self.advance()
        else:
            raise ParserError(f"expected expressionList or ')' after '(' in do statement, found '{next_type}': '{next_value}'")

        next_type, next_value = self.peek()
        if self.is_literal(next_type, next_value, ";"):
            self.advance()
        else:
            raise ParserError(f"do statement must end with ';', found '{next_type}': '{next_value}'")

        self.vm_writer.write_call(f"{callee}.{function_name}", n_args)
        self.vm_writer.write_pop("temp", 0)

        next_type, next_value = self.peek()
        if self.is_statement(next_type, next_value) or self.is_literal(next_type, next_value, "}"):
            self.advance()
        else:
            raise ParserError(f"'do' statement must be followed by another statement or '}}', found '{next_type}': '{next_value}'")

    def compile_let(self) -> None:
        next_type, next_value = self.peek()
        if self.is_identifier(next_type):
            self.advance()

            if self.current_value in self.symbol_table.scopes["subroutine"]:
                scope = "subroutine"
            else:
                scope = "class"

            var_segment = self.symbol_table.kind_of(scope, self.current_value)
            var_index = self.symbol_table.index_of(scope, self.current_value)

            is_array_assignment = False

        else:
            raise ParserError(f"expected identifier after 'let' in let statement, found '{next_type}': '{next_value}'")

        next_type, next_value = self.peek()
        if self.is_literal(next_type, next_value, "["):
            self.advance()

            is_array_assignment = True

            next_type, next_value = self.peek()
            if self.is_expression(next_type, next_value):
                self.advance()

                array_index_expression = self.compile_expression()
                util.order_expression(array_index_expression)
            
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

            expression = self.compile_expression()
            util.order_expression(expression)
            self.code_write(expression)

            if is_array_assignment:
                self.vm_writer.write_push(var_segment, var_index)
                self.code_write(array_index_expression)
                self.vm_writer.write_arithmetic("add")
                self.vm_writer.write_pop("pointer", 1)
                self.vm_writer.write_pop("that", 0)
            
            else:
                self.vm_writer.write_pop(var_segment, var_index)

        if not self.is_literal(self.current_type, self.current_value, ";"):
            raise ParserError(f"'let' statement must end with ';', found '{self.current_type}': '{self.current_value}'")

        next_type, next_value = self.peek()
        if self.is_statement(next_type, next_value) or self.is_literal(next_type, next_value, "}"):
            self.advance()
        else:
            raise ParserError(f"'let' statement must be followed by another statement or '}}', found '{next_type}': '{next_value}'")

    def compile_while(self) -> None:
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

        label_while_end, label_while_expression = self.generate_labels("while")
        expression = self.compile_expression()
        util.order_expression(expression)

        # VM code part 1
        self.vm_writer.write_label(label_while_expression)
        self.code_write(expression)
        self.vm_writer.write_arithmetic("not")
        self.vm_writer.write_if(label_while_end)
    
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
            self.compile_statements() # while statements
        elif self.is_literal(next_type, next_value, "}"):
            self.advance()
        else:
            raise ParserError(f"expected statement(s) or '}}' after '{{' in 'if' statement, found '{next_type}': '{next_value}'")

        # VM code part 2
        self.vm_writer.write_goto(label_while_expression)
        self.vm_writer.write_label(label_while_end)

        next_type, next_value = self.peek()
        if self.is_statement(next_type, next_value) or self.is_literal(next_type, next_value, "}"):
            self.advance()
        else:
            raise ParserError(f"'while' statement must be followed by another statement or '}}', found '{next_type}': '{next_value}'")

    def compile_return(self) -> None:
        next_type, next_value = self.peek()
        if self.is_expression(next_type, next_value):
            self.advance()

            expression = self.compile_expression()
            util.order_expression(expression)
            self.code_write(expression)
            self.vm_writer.write_return()
            
        elif self.is_literal(next_type, next_value, ";"): # void
            self.advance()
            self.vm_writer.write_push("constant", 0)
            self.vm_writer.write_return()
        else:
            raise ParserError(f"expected expression or ';' after 'return' in return statement, found '{next_type}': '{next_value}'")

        next_type, next_value = self.peek()
        if self.is_statement(next_type, next_value) or self.is_literal(next_type, next_value, "}"):
            self.advance()
        else:
            raise ParserError(f"'return' statement must be followed by another statement or '}}', found '{next_type}': '{next_value}'")

    def compile_if(self) -> None:
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

        label_if_end, label_if_false = self.generate_labels("if")
        expression = self.compile_expression()
        util.order_expression(expression)
        
        self.code_write(expression)
        self.vm_writer.write_arithmetic("not")
        self.vm_writer.write_if(label_if_false)

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
        else:
            raise ParserError(f"expected statement(s) or '}}' after '{{' in 'if' statement, found '{next_type}': '{next_value}'")
        
        self.vm_writer.write_goto(label_if_end)
        self.vm_writer.write_label(label_if_false)

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
            else:
                raise ParserError(f"expected statement(s) or '}}' after '{{' in else clause in 'if' statement, found '{next_type}': '{next_value}'")

        self.vm_writer.write_label(label_if_end)

        next_type, next_value = self.peek()
        if self.is_statement(next_type, next_value) or self.is_literal(next_type, next_value, "}"):
            self.advance()
        else:
            raise ParserError(f"'if' statement must be followed by another statement or '}}', found '{next_type}': '{next_value}'")

    def compile_expression_list(self) -> None:
        expression_list = []
        n_args = 1

        expression_list.append(self.compile_expression())

        while self.is_literal(self.current_type, self.current_value, ","):
            next_type, next_value = self.peek()
            if self.is_expression(next_type, next_value):
                self.advance()
                expression_list.append(self.compile_expression())
                n_args += 1
            else:
                raise ParserError(f"expected expression after ',' in expressionList, found '{next_type}': '{next_value}'")

        if not self.is_literal(self.current_type, self.current_value, ")"):
            raise ParserError(f"expressionList must close with ')', found '{self.current_type}': '{self.current_value}'")

        return n_args, expression_list

    def compile_expression(self) -> None:
        expression = []
        expression.append(self.compile_term())
        
        while self.is_operation(self.current_type, self.current_value):
            expression.append(self.current_value)
            next_type, next_value = self.peek()
            if self.is_term(next_type, next_value):
                self.advance()
                expression.append(self.compile_term())
            else:
                raise ParserError(f"expected term after '{self.current_value}' in expression, found '{next_type}': '{next_value}'")
                
        if not (
            self.is_literal(self.current_type, self.current_value, ",")
            or self.is_literal(self.current_type, self.current_value, ";")
            or self.is_literal(self.current_type, self.current_value, "]")
            or self.is_literal(self.current_type, self.current_value, ")")
        ):
            raise ParserError(f"expression must be followed by ',', ';', ']' or ')', found '{self.current_type}': '{self.current_value}'")

        return expression

    def compile_term(self) -> None:
        if self.is_keyword(self.current_type) or self.current_type == "integerConstant" or self.current_type == "stringConstant":
            term = self.current_value
            if self.current_type == "stringConstant":
                term = f"__STR_CONST__${term}"
            self.advance()
        
        elif self.is_literal(self.current_type, self.current_value, "-") or self.is_literal(self.current_type, self.current_value, "~"):
            term = self.current_value
            next_type, next_value = self.peek()
            if self.is_term(next_type, next_value):
                self.advance()
                if isinstance(term, list):
                    term.append(self.compile_term())
                else:
                    term = [term]
                    term.append(self.compile_term())
            else:
                raise ParserError(f"expected term after '{self.current_value}' in term, found '{next_type}': '{next_value}'")

        elif self.is_literal(self.current_type, self.current_value, "("):
            next_type, next_value = self.peek()
            if self.is_expression(next_type, next_value):
                self.advance()
                term = self.compile_expression()
            else:
                raise ParserError(f"expected expression after '(' in term, found '{next_type}': '{next_value}'")

            if not self.is_literal(self.current_type, self.current_value, ")"):
                raise ParserError(f"expected ')' after expression in term, found '{next_type}': '{next_value}'")
            
            self.advance()

        elif self.is_identifier(self.current_type):
            identifier_name = self.current_value
            next_type, next_value = self.peek()
            if self.is_literal(next_type, next_value, "."):
                self.advance()

                next_type, next_value = self.peek()
                if self.is_identifier(next_type):
                    self.advance()
                    term = f"{identifier_name}.{self.current_value}"
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
                    if isinstance(term, list):
                        term.append(self.compile_expression_list()[1])
                    else:
                        term = [term]
                        term.append(self.compile_expression_list()[1])

                elif self.is_literal(next_type, next_value, ")"):
                    self.advance()
                else:
                    raise ParserError(f"expected expressionList or ')' after '(' in function call within term, found '{next_type}': '{next_value}'")

            elif self.is_literal(next_type, next_value, "("):
                self.advance()
                term = {"class_method": f"{self.current_class}.{identifier_name}"}
                next_type, next_value = self.peek()
                if self.is_expression(next_type, next_value):
                    self.advance()
                    if isinstance(term, list):
                        term.append(self.compile_expression_list()[1])
                    else:
                        term = [term]
                        term.append(self.compile_expression_list()[1])

                elif self.is_literal(next_type, next_value, ")"):
                    self.advance()
                else:
                    raise ParserError(f"expected expressionList or ')' after '(' in method call within term, found '{next_type}': '{next_value}'")

            elif self.is_literal(next_type, next_value, "["):
                self.advance()
                term = {"array": identifier_name}
                next_type, next_value = self.peek()
                if self.is_expression(next_type, next_value):
                    self.advance()
                    if isinstance(term, list):
                        term.append(self.compile_expression())
                    else:
                        term = [term]
                        term.append(self.compile_expression())
                else:
                    raise ParserError(f"expected expression after '[' in array indexing within term, found '{next_type}': '{next_value}'")

            else:
                term = identifier_name

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

        return term
