from lexer import Lexer
from tabulate import tabulate

text_input = open("./input-code.abdo", "r").read()

# text_input = """
# x = 10.5 + y * (5 - 2.25);
# """

lexer = Lexer(code = text_input)
tokens = lexer.get_tokens()

print(f"Total number of lexemes and tokens: {len(tokens)}\n")

headers = ["Lexeme", "Token"]
print(tabulate(tokens, headers=headers, tablefmt="grid", stralign="center"))
