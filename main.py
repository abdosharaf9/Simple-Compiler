from lexer import Lexer
from simple_parser import Parser
from tabulate import tabulate

def print_title(title: str, end: str = "\n", before: str=None):
    if before != None:
        print(before, end="")
    print(f"{'=' * 7} {title} {'=' * 7}", end=end)


def get_input_code(from_file: bool=True) -> str:
    """ Get the input code that will be used. It can be a constant
    code string, input from user, or a text file that will be read.
    
    Args:
        from_file (bool): Flag to choose the source of input code.
        
    Returns:
        str: Source code to compile.
    """
    
    if from_file:
        input_code = open("./input-code.abdo", "r").read()
    else:
        input_code = """
        # This is a comment
        x = 10.5 + y * (5 - 2.25);
        if(x*2 >= 56/22) {
            if((y-1) > 2) {
                print(z);
            }
        }
        """
    
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
    parser = Parser(tokens=tokens)
    parsing_tree = parser.parse()
    return parsing_tree


def get_unordered_symbol_table():
    pass


def get_ordered_symbol_table():
    pass


def main():
    input_code = get_input_code()
    
    try:
        # Get tokens in the input code.
        tokens = lexical_analysis(code=input_code)
        
        # Print tokens in a table form.
        print_title(title="Lexical Analysis", before="\n")
        print(f"Total number of lexemes and tokens: {len(tokens)}\n")
        print(tabulate(tokens, headers=["Lexeme", "Token"], tablefmt="grid", stralign="center"))
        
        # Check code grammar using the parser and get the parsing tree.
        print_title(title="Parsing", before="\n")
        tree = parsing(tokens=tokens)
        print("This is a valid syntax!")
        
        print_title(title="Symbol Table", before="\n")
        
    except SyntaxError as se:
        print(se)


if __name__ == "__main__":
    main()