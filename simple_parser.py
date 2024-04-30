from lexer import Token
from tokens import *

class Parser:
    def __init__(self, tokens: list[Token]):
        self.tokens: list[Token] = tokens
        self.token_index: int = -1
        self.current_token: Token = None
        self.advance()


    def match(self, token_type: str):
        if self.current_token.token_type == token_type:
            self.advance()
        else:
            raise SyntaxError(f"⚠️  Syntax Error in <{self.current_token.lexeme}>! Expected <{token_type}> but found <{self.current_token.token_type}>")


    def advance(self):
        self.token_index += 1
        if self.token_index < len(self.tokens):
            self.current_token = self.tokens[self.token_index]
        else:
            self.current_token = None


    def parse(self):
        self.stmt_list()


    def stmt_list(self):
        while self.current_token != None:
            self.stmt()


    def stmt(self):
        if self.current_token.token_type == DATA_TYPE:
            self.validate_dec_stmt()
        elif self.current_token.token_type == ID:
            self.validate_assign_stmt()
        elif self.current_token.lexeme == "print" and self.current_token.token_type == KEYWORD:
            self.validate_print_stmt()
        elif self.current_token.lexeme == "if" and self.current_token.token_type == KEYWORD:
            self.validate_if_stmt()
        else:
            raise SyntaxError(f"⚠️  Syntax Error in <{self.current_token.lexeme}>! Unexpected token <{self.current_token.token_type}>")


    def validate_dec_stmt(self):
        self.match(DATA_TYPE)
        self.match(ID)
        if self.current_token.token_type == ASSIGN:
            self.match(ASSIGN)
            self.validate_arth_expr()
        self.match(SEMICOLON)


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
        while self.current_token.token_type == ARITHMETIC_OPERATOR:
            self.advance()
            self.validate_term()


    def validate_term(self):
        if self.current_token.token_type in [ID, NUMBER]:
            self.advance()
        elif self.current_token.token_type == LEFT_PAREN:
            self.match(LEFT_PAREN)
            self.validate_arth_expr()
            self.match(RIGHT_PAREN)
        else:
            raise SyntaxError(f"⚠️  Syntax Error in <{self.current_token.lexeme}>! Not a valid expression!")

