from lexer import Token
from tokens import *

class Node:
    def __init__(self, type):
        self.type = type
        self.children = []

    def add_child(self, node):
        self.children.append(node)
    
    def print_tree(self, file, level=0):
        # print("\t" * level + self.type)
        file.write("\t" * level + self.type + "\n")
        for child in self.children:
            child.print_tree(file, level + 1)


class Parser:
    def __init__(self, tokens: list[Token]):
        self.tokens: list[Token] = tokens
        self.token_index: int = -1
        self.current_token: Token = None
        self.root: Node = None
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
        self.root = self.stmt_list()


    def stmt_list(self) -> Node:
        root = Node("stmt_list")
        
        while self.current_token != None:
            root.add_child(self.stmt())
        
        return root


    def stmt(self) -> Node:
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


    def validate_dec_stmt(self) -> Node:
        node = Node("dec_stmt")
        
        node.add_child(Node(self.current_token.token_type))
        self.match(DATA_TYPE)
        
        node.add_child(Node(self.current_token.token_type))
        self.match(ID)
        
        if self.current_token.token_type == ASSIGN:
            node.add_child(Node(self.current_token.token_type))
            self.match(ASSIGN)
            
            node.add_child(self.validate_arth_expr())
        
        node.add_child(Node(self.current_token.token_type))
        self.match(SEMICOLON)
        
        return node


    def validate_assign_stmt(self) -> Node:
        node = Node("assign_stmt")
        node.add_child(Node(self.current_token.token_type))
        self.match(ID)
        
        node.add_child(Node(self.current_token.token_type))
        self.match(ASSIGN)
        
        node.add_child(self.validate_arth_expr())
        
        node.add_child(Node(self.current_token.token_type))
        self.match(SEMICOLON)
        
        return node


    def validate_print_stmt(self) -> Node:
        node = Node("print_stmt")
        node.add_child(Node(self.current_token.token_type))
        self.match(KEYWORD)
        
        node.add_child(Node(self.current_token.token_type))
        self.match(LEFT_PAREN)
        
        node.add_child(Node(self.current_token.token_type))
        self.match(ID)
        
        node.add_child(Node(self.current_token.token_type))
        self.match(RIGHT_PAREN)
        
        node.add_child(Node(self.current_token.token_type))
        self.match(SEMICOLON)
        
        return node


    def validate_if_stmt(self) -> Node:
        node = Node("if_stmt")
        node.add_child(Node(self.current_token.token_type))
        self.match(KEYWORD)
        
        node.add_child(Node(self.current_token.token_type))
        self.match(LEFT_PAREN)
        
        node.add_child(self.validate_rel_expr())
        
        node.add_child(Node(self.current_token.token_type))
        self.match(RIGHT_PAREN)
        
        node.add_child(Node(self.current_token.token_type))
        self.match(LEFT_BRACE)
        
        node.add_child(self.stmt())
        
        node.add_child(Node(self.current_token.token_type))
        self.match(RIGHT_BRACE)
        
        return node


    def validate_rel_expr(self) -> Node:
        node = Node("rel_expr")
        
        node.add_child(self.validate_arth_expr())
        
        node.add_child(Node(self.current_token.token_type))
        self.match(RELATIONAL_OPERATOR)
        
        node.add_child(self.validate_arth_expr())
        
        return node


    def validate_arth_expr(self) -> Node:
        node = Node("arth_expr")
        
        node.add_child(self.validate_term())
        
        while self.current_token.token_type == ARITHMETIC_OPERATOR:
            node.add_child(Node(self.current_token.token_type))
            self.advance()
            
            node.add_child(self.validate_term())

        return node


    def validate_term(self) -> Node:
        node = Node("term")
        
        if self.current_token.token_type in [ID, NUMBER]:
            node.add_child(Node(self.current_token.token_type))
            self.advance()
        elif self.current_token.token_type == LEFT_PAREN:
            node.add_child(Node(self.current_token.token_type))
            self.match(LEFT_PAREN)
            
            node.add_child(self.validate_arth_expr())
            
            node.add_child(Node(self.current_token.token_type))
            self.match(RIGHT_PAREN)
        else:
            raise SyntaxError(f"⚠️  Syntax Error in <{self.current_token.lexeme}>! Not a valid expression!")
        
        return node
