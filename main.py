from lexer import Lexer, Token
from simple_parser import Parser, Node
from symbol_table import SymbolTable, HashSymbolTable, get_tree_symbol_table, print_tree_table
from tokens import ID
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


def lexical_analysis(code: str) -> list[Token]:
    """Do Lexical analysis to the input code and get tokens, and
    lexemes in it.

    Args:
        code (str): The input code we will analyze.

    Returns:
        list[Token]: The list of tokens and lexemes in the code.
    """
    lexer = Lexer(code = code)
    tokens = lexer.get_tokens()
    return tokens


def parsing(tokens: list[Token]) -> Node:
    parser = Parser(tokens=tokens)
    parser.parse()
    parsing_tree = parser.root
    return parsing_tree


def get_ids(tokens: list[Token]) -> list[str]:
    id_tokens = filter(lambda x: x.token_type == ID, tokens)
    return list(set(map(lambda x: x.lexeme, id_tokens)))


def main():
    input_code = get_input_code()
    
    try:
        # Get tokens in the input code.
        tokens = lexical_analysis(code=input_code)
        
        # Print tokens in a table form.
        print_title(title="Lexical Analysis", before="\n")
        print(f"Total number of lexemes and tokens: {len(tokens)}\n")
        tokens_to_print = [(token.lexeme, token.token_type) for token in tokens]
        print(tabulate(tokens_to_print, headers=["Lexeme", "Token"], tablefmt="grid", stralign="center"))
        
        # Check code grammar using the parser and get the parsing tree.
        print_title(title="Parsing", before="\n")
        tree = parsing(tokens=tokens)
        print("This is a valid syntax!")
        
        print("For the parsing tree, see the \"output_tree.txt\" file.")
        with open("output_tree.txt", "w") as file_output:
            tree.print_tree(file_output)
        
        # # Get unordered and ordered symbol table.
        symbol_table = SymbolTable(tokens)
        unordered = symbol_table.get_unordered_symbol_table()
        ordered = symbol_table.get_ordered_symbol_table()
        
        headers = ["Id", "Data Type", "Delaration Line", "Reference Lines", "Address", "Scope", "Dimension"]
        
        # print unordered symbol table in table form.
        print_title(title="Unordered Symbol Table", before="\n")
        print(tabulate(unordered.values(), headers=headers, tablefmt="grid", stralign="center", numalign="center"))
        
        # print ordered symbol table in table form.
        print_title(title="Ordered Symbol Table", before="\n")
        print(tabulate(ordered.values(), headers=headers, tablefmt="grid", stralign="center", numalign="center"))
        
        # print ids only from tokens, form tree symbol table, and print it.
        ids = get_ids(tokens)
        tree = get_tree_symbol_table(ids)
        print_title(title="Tree Structured Symbol Table", before="\n")
        print_tree_table(tree)
        
        print_title(title="Hash Symbol Table", before="\n")
        hash_table = HashSymbolTable(ids)
        hash_table.print_hash_table()
        
    except SyntaxError as se:
        print(se)
    except ValueError as ve:
        print(ve)


if __name__ == "__main__":
    main()