from lexer import Lexer
from tabulate import tabulate

def get_input_code() -> str:
    """ Get the input code that will be used. It can be a constant
    code string, input from user, or a text file that will be read.
    """
    input_code = open("./input-code.abdo", "r").read()

    # input_code = """
    # x = 10.5 + y * (5 - 2.25);
    # """
    
    return input_code


def lexical_analysis(code: str) -> list[tuple[str, str]]:
    """Do Lexical analysis to the input code and get tokens, and
    lexemes in it.

    Args:
        code (str): The input code we will analyze.

    Returns:
        list[tuple[str, str]]: The list of tokens and lexemes in the code.
    """
    lexer = Lexer(code = code)
    tokens = lexer.get_tokens()
    return tokens


def parsing(tokens: list[tuple[str, str]]):
    pass


def get_unordered_symbol_table():
    pass


def get_ordered_symbol_table():
    pass


def main():
    try:
        input_code = get_input_code()
        
        # Get tokens in the input code and print them in a table
        tokens = lexical_analysis(code=input_code)
        print(f"Total number of lexemes and tokens: {len(tokens)}\n")
        print(tabulate(tokens, headers=["Lexeme", "Token"], tablefmt="grid", stralign="center"))
        
        
    except SyntaxError as se:
        print(se)


if __name__ == "__main__":
    main()