from lexer import Token
from tokens import *
from dataclasses import dataclass
from PrettyPrint import PrettyPrintTree
from colorama import Back

@dataclass
class SymbolTableEntry:
    """Used to save single table entry."""
    name: str
    data_type: str
    declaration_line: int
    reference_lines: list[int]
    address: int
    scope: str = "Global"
    dimension: int = 0 # Because all variables are primitives.

    def add_reference_line(self, line):
        self.reference_lines.append(line)


class SymbolTable:
    def __init__(self, tokens: list[Token]):
        """Initialize the tables with an empty dictionary, and use the
        tokens list to build the tables.

        Args:
            tokens (list[Token]): The list of tokens in the code.
        """
        self.tokens: list[Token] = tokens
        self.unordered_table: dict[str, SymbolTableEntry] = {}
        self.ordered_table: dict[str, SymbolTableEntry] = {}
        self.address: int = 0 # The initial address.
        self.build_unordered_symbol_table()
        self.build_ordered_symbol_table()


    def insert(self, name: str, data_type: str, line: int, scope: str):
        """Used to insert or update an ID entity in the table. If the
        ID is already in the table, just update the reference lines. If
        the ID wasn't added before, add a new entity for it. 

        Args:
            name (str): ID name.
            data_type (str): ID data type.
            line (int): Current line.
            scope (str): ID scope.
        """
        if name in self.unordered_table:
            # The Id was already added to the table just 
            # update the reference lines.
            entry = self.add_reference(name=name, line=line)
        else:
            # The Id is new. Create a new entity for it.
            entry = SymbolTableEntry(
                name=name,
                data_type=data_type,
                declaration_line=line,
                reference_lines=[],
                address=self.address,
                scope=scope
            )
            
            # Update address
            self.address += 2
        
        # Update the Id object in the table.
        self.unordered_table[name] = entry

    
    def add_reference(self, name: str, line: int) -> SymbolTableEntry:
        """Update the reference lines of the ID and return it back.

        Args:
            name (str): ID name.
            line (int): Reference line number.

        Returns:
            SymbolTableEntry: The updated ID entity.
        """
        entry = self.unordered_table[name]
        entry.add_reference_line(line)
        return entry

    
    def build_unordered_symbol_table(self):
        """Uses the tokens list to build an unordered symbol table.

        Raises:
            SyntaxError: If a variable is used before declaration, raise a
            syntax error to inform the user with the error in details.
        """
        # Used to track the variables types and scope.
        current_data_type = None
        current_scope = "Global"
        opened_braces = 0

        for token in self.tokens:
            if token.token_type == DATA_TYPE:
                current_data_type = token.lexeme
            elif token.token_type == ID:
                # If the current token is ID, check if it's declared.
                if current_data_type:
                    self.insert(name=token.lexeme, data_type=current_data_type, line=token.line_number, scope=current_scope)
                    current_data_type = None
                elif token.lexeme in self.unordered_table:
                    self.insert(name=token.lexeme, data_type=None, line=token.line_number, scope=current_scope)
                else:
                    raise SyntaxError(f"⚠️  The variable <{token.lexeme}> is used before being declared!")
            
            # Count opened barces for local variables.
            elif token.token_type == LEFT_BRACE:
                opened_braces += 1
            elif token.token_type == RIGHT_BRACE:
                opened_braces -= 1

            # Change the current scope according to the braces.
            if opened_braces == 0: current_scope = "Global"
            else: current_scope = "Local"


    def build_ordered_symbol_table(self):
        """Build the ordered symbol table using the unordered
        version after sorting the IDs alphabeticaly."""
        self.ordered_table = dict(sorted(self.unordered_table.items(), key=lambda item: item[0]))


class TreeTableNode:
    """Used to present a node in the Tree-Structured symbol
    table, which is a binary tree."""
    def __init__(self, value: str):
        self.value: str = value
        self.left_child: TreeTableNode = None
        self.right_child: TreeTableNode = None


class TreeSymbolTable:
    def __init__(self, ids: list[str]) -> None:
        """Initialize the table with the tokens list and use it to
        build the tree symbol table.

        Args:
            ids (list[str]): The list of IDs tokens.
        """
        self.ids: list[str] = ids
        self.root: TreeTableNode = self.build_tree_symbol_table()


    def build_tree_symbol_table(self) -> TreeTableNode:
        """Initialize the root with the first ID and loop over
        the rest of IDs to insert them as a children to it.

        Returns:
            TreeTableNode: The tree root.
        """
        root = TreeTableNode(self.ids[0])
    
        for token in self.ids[1:]:
            self.insert_node(root, token)
        
        return root
    
    
    def insert_node(self, root: TreeTableNode, token: str) -> TreeTableNode:
        """Insert children nodes recursively into the root according
        to their alphabetical order.

        Args:
            root (TreeTableNode): The root node.
            token (str): The ID which will be the node value.

        Returns:
            TreeTableNode: The root node after adding its children.
        """
        if root is None: return TreeTableNode(token)
        
        if token < root.value:
            root.left_child = self.insert_node(root.left_child, token)
        else:
            root.right_child = self.insert_node(root.right_child, token)
        
        return root


    def print_tree_table(self):
        """Used to print the tree in a pretty way."""
        pt = PrettyPrintTree(
            get_children=lambda node: [] if node is None or node.left_child is node.right_child is None else [node.left_child, node.right_child],
            get_val=lambda node: node.value if node else None,
            color=Back.BLUE
        )
        pt(self.root)


class HashSymbolTable:
    def __init__(self, ids: list[str]):
        """Initialize the table using an empty dictionary, and use
        the list of IDs to build it.

        Args:
            ids (list[str]): The list of IDs in the tokens.
        """
        self.ids: list[str] = ids
        self.table: dict[int, list[str]] = {}
        self.insert_all()
        

    def hash_function(self, id: str) -> int:
        """Get the hash value for the given ID.

        Args:
            id (str): The ID we need to calculate the hash value.

        Returns:
            int: The hash value.
        """
        return (len(id) + ord(id[0])) % len(self.ids)
    
    
    def get_all_hash_values(self) -> list[int]:
        """Get all the hash values.

        Returns:
            list[int]: List of hash values.
        """
        return [self.hash_function(id) for id in self.ids]
    
    
    def insert_all(self):
        """Insert all the IDs in the dictionary according to
        their hash values."""
        hash_indeces = self.get_all_hash_values()
        
        # Loop over the IDs to add each one in its hash
        # value in the table.
        for i, id in enumerate(self.ids):
            index = hash_indeces[i]
            
            # Initialize the hash value with an empty list.
            if index not in self.table:
                self.table[index] = []

            # Add the ID to its hash value list.
            self.table[index].append(id)
    
    
    def print_hash_table(self):
        """Used to print the hash values with the list of each one of them."""
        for index, values in self.table.items():
            print(index, end=" --> ")
            
            for value in values:
                if value != values[-1]: print(value, end=" --> ")
                else: print(value)

