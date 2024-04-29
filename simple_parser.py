import re
from lexer import Lexer
from tokens import *

class Parser:
    def __init__(self, tokens: list[tuple[str, str]]):
        self.tokens: list[tuple[str, str]] = tokens
        self.token_index: int = -1
        self.current_token: tuple[str, str] = None
        self.advance()


    def match(self, token_type: str):
        if self.current_token[1] == token_type:
            self.advance()
        else:
            raise SyntaxError(f"⚠️  Syntax Error in <{self.current_token[0]}>! Expected <{token_type}> but found <{self.current_token[1]}>")


    def advance(self):
        self.token_index += 1
        if self.token_index < len(self.tokens):
            self.current_token = self.tokens[self.token_index]
        else:
            self.current_token = (EOF, EOF)


    def parse(self):
        self.stmt_list()


    def stmt_list(self):
        while self.current_token != (EOF, EOF):
            self.stmt()


    def stmt(self):
        if self.current_token[1] == ID:
            self.validate_assign_stmt()
        elif self.current_token == ("print", KEYWORD):
            self.validate_print_stmt()
        elif self.current_token == ("if", KEYWORD):
            self.validate_if_stmt()
        else:
            raise SyntaxError(f"⚠️  Syntax Error in <{self.current_token[0]}>! Unexpected token <{self.current_token[1]}>")


    def validate_assign_stmt(self):
        self.match(ID)
        self.match(ASSIGN)
        self.validate_arth_expr()
        self.match(SEMICOLON)


    def validate_print_stmt(self):
        self.match(KEYWORD)
        self.match(LEFT_PAREN)
        self.match(ID)
        self.match(RIGHT_PAREN)
        self.match(SEMICOLON)


    def validate_if_stmt(self):
        self.match(KEYWORD)
        self.match(LEFT_PAREN)
        self.validate_rel_expr()
        self.match(RIGHT_PAREN)
        self.match(LEFT_BRACE)
        self.stmt()
        self.match(RIGHT_BRACE)


    def validate_rel_expr(self):
        self.validate_arth_expr()
        self.match(RELATIONAL_OPERATOR)
        self.validate_arth_expr()


    def validate_arth_expr(self):
        self.validate_term()
        while self.current_token[1] == ARITHMETIC_OPERATOR:
            self.advance()
            self.validate_term()


    def validate_term(self):
        if self.current_token[1] in [ID, NUMBER]:
            self.advance()
        elif self.current_token[1] == LEFT_PAREN:
            self.match(LEFT_PAREN)
            self.validate_arth_expr()
            self.match(RIGHT_PAREN)
        else:
            raise SyntaxError(f"⚠️  Syntax Error in <{self.current_token[0]}>! Not a valid expression!")

