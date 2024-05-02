from lexer import Lexer, Token
from simple_parser import Parser, ParsingTreeNode
from symbol_table import SymbolTable, HashSymbolTable, TreeSymbolTable
from tokens import ID
from tabulate import tabulate

def print_title(title: str, end: str = "\n", before: str=None):
    """Used to print output title in a nice way.

    Args:
        title (str): The title you want to print
        end (str, optional): Text after title. Defaults to "\\n".
        before (str, optional): Text before title. Defaults to None.
    """
    if before != None: print(before, end="")
    print(f"{'=' * 10} {title} {'=' * 10}", end=end)


def get_input_code(from_file: bool=True) -> str:
    """ Get the input code that will be used. It can be a constant
    code string, input from user, or a text file that will be read.
    
    Args:
        from_file (bool): Flag to choose the source of input code.
        
    Returns:
        str: Source code to compile.
    """
    
    if from_file:
        input_code = open("./test.abdo", "r").read()
    else:
        input_code = """
        # This is a comment
        float y = 1.5;
        int x = 2024;
        int z = 10.5 + y * (x - 2.25);
        if(x*2 >= 56/22) {
            if((y-1) > 2) {
                print(z);
            }
        }
        """
    
    return input_code


def lexical_analysis(code: str) -> list[Token]:
    """Do Lexical analysis to the input code and get tokens &
    lexemes in it.

    Args:
        code (str): The input code we will analyze.

    Returns:
        list[Token]: The list of tokens and lexemes in the code.
    """
    lexer = Lexer(code = code)
    tokens = lexer.get_tokens()
    return tokens


def do_parsing(tokens: list[Token]) -> ParsingTreeNode:
    """Do parsing to the tokens list to check the grammar, and
    return the parsing tree.

    Args:
        tokens (list[Token]): The list of tokens in the code.

    Returns:
        Node: Parsing tree root.
    """
    parser = Parser(tokens=tokens)
    parser.parse()
    return parser.parsing_tree_root


def get_ids_names(tokens: list[Token]) -> list[str]:
    """Filter the tokens to get the ID names only.

    Args:
        tokens (list[Token]): The list of tokens.

    Returns:
        list[str]: The ID names list with non duplicated IDs.
    """
    id_tokens = filter(lambda x: x.token_type == ID, tokens)
    id_names = list(map(lambda x: x.lexeme, id_tokens))
    non_duplicated_ids = [id for i, id in enumerate(id_names) if id not in id_names[:i]]
    return non_duplicated_ids


def print_tokens(tokens: list[Token]):
    """Print tokens list in a fancy table form.

    Args:
        tokens (list[Token]): The tokens list.
    """
    print_title(title="Lexical Analysis", before="\n")
    print(f"Total number of lexemes & tokens = {len(tokens)}\n")
    tokens_to_print = [(token.lexeme, token.token_type) for token in tokens]
    print(tabulate(tokens_to_print, headers=["Lexeme", "Token"], tablefmt="rounded_grid", stralign="center"))


def parse_and_print_tree(tokens: list[Token]):
    """Takes the list of tokens in the code, parse it to check
    the syntax of the code according to the grammar, and then
    print the parsing tree.

    Args:
        tokens (list[Token]): The list of tokens in the code.
    """
    print_title(title="Parsing", before="\n")
    parsing_tree = do_parsing(tokens=tokens)
    
    # If there is no error in the code, this will be printed.
    print("This is a valid syntax!")
    
    # Print parsing tree in a text file to save space in the terminal.
    print("For the parsing tree, see the \"output_tree.txt\" file.")
    with open("output_tree.txt", "w") as output_file:
        parsing_tree.print_tree(output_file)


def print_symbol_tables(tokens: list[Token]):
    """Takes the list of tokens in the code and print the four
    types of symbol table (Unordered, Ordered, Tree-Structured, Hash).

    Args:
        tokens (list[Token]): The list of tokens.
    """
    
    # Form unordered and ordered symbol tables.
    symbol_table = SymbolTable(tokens)
    headers = ["Id", "Data Type", "Delaration Line", "Reference Lines", "Address", "Scope", "Dimension"]
    
    # Print unordered symbol table in table form.
    print_title(title="Unordered Symbol Table", before="\n")
    print(tabulate(symbol_table.unordered_table.values(), headers=headers, tablefmt="rounded_grid", stralign="center", numalign="center"))
    
    # Print ordered symbol table in table form.
    print_title(title="Ordered Symbol Table", before="\n")
    print(tabulate(symbol_table.ordered_table.values(), headers=headers, tablefmt="rounded_grid", stralign="center", numalign="center"))
    
    # Get ids only from tokens.
    ids = get_ids_names(tokens)
    
    # Form tree symbol table and print it.
    tree_table = TreeSymbolTable(ids=ids)
    print_title(title="Tree Structured Symbol Table", before="\n")
    tree_table.print_tree_table()
    
    # Form hash symbol table and print it.
    print_title(title="Hash Symbol Table", before="\n")
    hash_table = HashSymbolTable(ids)
    hash_table.print_hash_table()


def main():
    input_code = get_input_code()
    
    try:
        # Get tokens in the input code, and print them in a table form.
        tokens = lexical_analysis(code=input_code)
        print_tokens(tokens)
        
        # Check code grammar using the parser and print the parsing tree.
        parse_and_print_tree(tokens)
        
        # Get symbol tables and print them.
        print_symbol_tables(tokens)
    
    # Catch errors in the code to print them.
    except SyntaxError as se:
        print(se)


if __name__ == "__main__":
    main()