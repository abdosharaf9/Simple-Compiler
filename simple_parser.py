from lexer import Token
from tokens import *

class ParsingTreeNode:
    def __init__(self, title: str):
        self.title: str = title
        self.children: list[ParsingTreeNode] = []

    def add_child(self, node):
        self.children.append(node)
    
    def print_tree(self, file, level: int = 0):
        # Write current node into the file.
        file.write("\t" * level + self.title + "\n")
        
        # Write each child in the current node.
        for child in self.children:
            child.print_tree(file, level + 1)


class Parser:
    def __init__(self, tokens: list[Token]):
        self.tokens: list[Token] = tokens
        self.token_index: int = -1
        self.current_token: Token = None
        self.parsing_tree_root: ParsingTreeNode = None
        self.advance()


    def match(self, token_type: str):
        """Used to match the current token with the needed token type.

        Args:
            token_type (str): Needed token type.

        Raises:
            SyntaxError: If the current token is not matched as we need,
            raise a syntax error to inform the user with the error in details.
        """
        if self.current_token.token_type == token_type:
            self.advance()
        else:
            raise SyntaxError(f"⚠️  Syntax Error in <{self.current_token.lexeme}>! Expected <{token_type}> but found <{self.current_token.token_type}>")


    def advance(self):
        """Used to read the next token in the list. If there no next token,
        assign None to stop the parsing."""
        self.token_index += 1
        
        if self.token_index < len(self.tokens):
            self.current_token = self.tokens[self.token_index]
        else:
            self.current_token = None


    def parse(self):
        """Start parsing the tokens and building the parsing tree."""
        self.parsing_tree_root = self.stmt_list()


    def stmt_list(self) -> ParsingTreeNode:
        """Used to parse statement list. It loops over the program
        statements and parse each one. Also, add each statement as
        a child node to the root node in the parsing tree.

        Returns:
            ParsingTreeNode: The root node of the parsing tree.
        """
        root = ParsingTreeNode("stmt_list")
        
        while self.current_token != None:
            root.add_child(self.validate_stmt())
        
        return root


    def validate_stmt(self) -> ParsingTreeNode:
        """Used to parse a single statement of the program accroding to the
        grammar of the language. Each statement will be a node and returned
        to be a child of the program.

        Raises:
            SyntaxError: If the current statement doesn't belong to the
            language grammar, raise a syntax error to inform the user
            with the error in details.

        Returns:
            ParsingTreeNode: The statment as node to be a child in the tree.
        """
        
        # Check if the statement is one of the four statements in the grammar.
        if self.current_token.token_type == DATA_TYPE:
            return self.validate_dec_stmt()
        elif self.current_token.token_type == ID:
            return self.validate_assign_stmt()
        elif self.current_token.lexeme == "print" and self.current_token.token_type == KEYWORD:
            return self.validate_print_stmt()
        elif self.current_token.lexeme == "if" and self.current_token.token_type == KEYWORD:
            return self.validate_if_stmt()
        else:
            raise SyntaxError(f"⚠️  Syntax Error in <{self.current_token.lexeme}>! Unexpected token <{self.current_token.token_type}>")


    def validate_dec_stmt(self) -> ParsingTreeNode:
        """Validate if the current statement is a declaration statement
        according to the grammar.

        Returns:
            ParsingTreeNode: Declaration statement node.
        """
        # The root will be the declaration statement itself.
        node = ParsingTreeNode("dec_stmt")
        
        # Check for each part in the statement and add it as a child
        # to the statement node.
        node.add_child(ParsingTreeNode(f"{self.current_token.token_type}({self.current_token.lexeme})"))
        self.match(DATA_TYPE)
        
        node.add_child(ParsingTreeNode(f"{self.current_token.token_type}({self.current_token.lexeme})"))
        self.match(ID)
        
        # Because we can declare without giving a value.
        if self.current_token.token_type == ASSIGN:
            node.add_child(ParsingTreeNode(f"{self.current_token.token_type}({self.current_token.lexeme})"))
            self.match(ASSIGN)
            
            node.add_child(self.validate_arth_expr())
        
        node.add_child(ParsingTreeNode(f"{self.current_token.token_type}({self.current_token.lexeme})"))
        self.match(SEMICOLON)
        
        return node


    def validate_assign_stmt(self) -> ParsingTreeNode:
        """Validate if the current statement is an assignment statement
        according to the grammar.

        Returns:
            ParsingTreeNode: Assignment statement node.
        """
        # The root will be the assignment statement itself.
        node = ParsingTreeNode("assign_stmt")
        
        # Check for each part in the statement and add it as a child
        # to the statement node.
        node.add_child(ParsingTreeNode(f"{self.current_token.token_type}({self.current_token.lexeme})"))
        self.match(ID)
        
        node.add_child(ParsingTreeNode(f"{self.current_token.token_type}({self.current_token.lexeme})"))
        self.match(ASSIGN)
        
        node.add_child(self.validate_arth_expr())
        
        node.add_child(ParsingTreeNode(f"{self.current_token.token_type}({self.current_token.lexeme})"))
        self.match(SEMICOLON)
        
        return node


    def validate_print_stmt(self) -> ParsingTreeNode:
        """Validate if the current statement is a print statement
        according to the grammar.

        Returns:
            ParsingTreeNode: Print statement node.
        """
        # The root will be the print statement itself.
        node = ParsingTreeNode("print_stmt")
        
        # Check for each part in the statement and add it as a child
        # to the statement node.
        node.add_child(ParsingTreeNode(f"{self.current_token.token_type}({self.current_token.lexeme})"))
        self.match(KEYWORD)
        
        node.add_child(ParsingTreeNode(f"{self.current_token.token_type}({self.current_token.lexeme})"))
        self.match(LEFT_PAREN)
        
        node.add_child(ParsingTreeNode(f"{self.current_token.token_type}({self.current_token.lexeme})"))
        self.match(ID)
        
        node.add_child(ParsingTreeNode(f"{self.current_token.token_type}({self.current_token.lexeme})"))
        self.match(RIGHT_PAREN)
        
        node.add_child(ParsingTreeNode(f"{self.current_token.token_type}({self.current_token.lexeme})"))
        self.match(SEMICOLON)
        
        return node


    def validate_if_stmt(self) -> ParsingTreeNode:
        """Validate if the current statement is an if statement
        according to the grammar.

        Returns:
            ParsingTreeNode: If statement node.
        """
        # The root will be the if statement itself.
        node = ParsingTreeNode("if_stmt")
        
        # Check for each part in the statement and add it as a child
        # to the statement node.
        node.add_child(ParsingTreeNode(f"{self.current_token.token_type}({self.current_token.lexeme})"))
        self.match(KEYWORD)
        
        node.add_child(ParsingTreeNode(f"{self.current_token.token_type}({self.current_token.lexeme})"))
        self.match(LEFT_PAREN)
        
        node.add_child(self.validate_rel_expr())
        
        node.add_child(ParsingTreeNode(f"{self.current_token.token_type}({self.current_token.lexeme})"))
        self.match(RIGHT_PAREN)
        
        node.add_child(ParsingTreeNode(f"{self.current_token.token_type}({self.current_token.lexeme})"))
        self.match(LEFT_BRACE)
        
        node.add_child(self.validate_stmt())
        
        node.add_child(ParsingTreeNode(f"{self.current_token.token_type}({self.current_token.lexeme})"))
        self.match(RIGHT_BRACE)
        
        return node


    def validate_rel_expr(self) -> ParsingTreeNode:
        """Validate if the current expression is a relational
        expression according to the grammar.

        Returns:
            ParsingTreeNode: Relational expression node.
        """
        # The root will be the relational expression itself.
        node = ParsingTreeNode("rel_expr")
        
        # Check for each part in the expression and add it as a child
        # to the expression node.
        node.add_child(self.validate_arth_expr())
        
        node.add_child(ParsingTreeNode(f"{self.current_token.token_type}({self.current_token.lexeme})"))
        self.match(RELATIONAL_OPERATOR)
        
        node.add_child(self.validate_arth_expr())
        
        return node


    def validate_arth_expr(self) -> ParsingTreeNode:
        """Validate if the current expression is an arithmetic
        expression according to the grammar.

        Returns:
            ParsingTreeNode: Arithmetic expression node.
        """
        # The root will be the arithmetic expression itself.
        node = ParsingTreeNode("arth_expr")
        
        # Check for each part in the expression and add it as a child
        # to the expression node.
        node.add_child(self.validate_term())
        
        # Used for the expressions like (x + 5).
        while self.current_token.token_type == ARITHMETIC_OPERATOR:
            node.add_child(ParsingTreeNode(f"{self.current_token.token_type}({self.current_token.lexeme})"))
            self.advance()
            node.add_child(self.validate_term())

        return node


    def validate_term(self) -> ParsingTreeNode:
        """Validate if the current piece of code is a term
        according to the grammar.

        Raises:
            SyntaxError: If the code doesn't match the term form, raise
            a syntax error to inform the user with the error in details.

        Returns:
            ParsingTreeNode: Term node.
        """
        # The root will be the term itself.
        node = ParsingTreeNode("term")
        
        # Check for the term cases and add them as children to the
        # term node.
        if self.current_token.token_type in [ID, NUMBER]:
            node.add_child(ParsingTreeNode(f"{self.current_token.token_type}({self.current_token.lexeme})"))
            self.advance()
        elif self.current_token.token_type == LEFT_PAREN:
            node.add_child(ParsingTreeNode(f"{self.current_token.token_type}({self.current_token.lexeme})"))
            self.match(LEFT_PAREN)
            
            node.add_child(self.validate_arth_expr())
            
            node.add_child(ParsingTreeNode(f"{self.current_token.token_type}({self.current_token.lexeme})"))
            self.match(RIGHT_PAREN)
        else:
            raise SyntaxError(f"⚠️  Syntax Error in <{self.current_token.lexeme}>! Not a valid expression!")
        
        return node
