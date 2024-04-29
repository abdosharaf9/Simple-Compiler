import re
from lexer import Lexer
from tokens import *

class Parser:
    def __init__(self, tokens: list[tuple[str, str]]):
        self.tokens: list[tuple[str, str]] = tokens
        self.token_index: int = -1
        self.current_token: tuple[str, str] = None
        self.advance()


    def parse(self):
        while self.current_token[0] != EOF:
            self.stmt()


    def stmt(self):
        self.match(ID)
        self.match(ASSIGN)
        self.expr()
        self.match(SIMI_COLON)


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


    def expr(self):
        self.term()
        while self.current_token[1] == ARITHMETIC_OPERATOR:
            self.advance()
            self.term()


    def term(self):
        if self.current_token[1] in [ID, INT, FLOAT]:
            self.advance()
        elif self.current_token[1] == LEFT_PAREN:
            self.match(LEFT_PAREN)
            self.expr()
            self.match(RIGHT_PAREN)
        else:
            raise SyntaxError(f"⚠️  Syntax Error in <{self.current_token[0]}>! Not a valid expression!")


input_code = open("./input-code.abdo", "r").read()
lexer = Lexer(code=input_code)
tokens = lexer.get_tokens()
print(tokens, end="\n\n\n")
parser = Parser(tokens=tokens)
try:
    parser.parse()
except SyntaxError as se:
    print(se)