from lexer import Token
from tokens import *
from dataclasses import dataclass

@dataclass
class SymbolTableEntry:
    name: str
    data_type: str
    line_declaration: int
    usage_lines: list[int]
    address: str
    scope: str = "Global"
    dimension: int = 1

    def add_usage_line(self, line):
        self.usage_lines.append(line)


class SymbolTable:
    def __init__(self, tokens: list[Token]):
        self.tokens: list[Token] = tokens
        self.unordered_table: dict[str, SymbolTableEntry] = {}
        self.ordered_table: dict[str, SymbolTableEntry] = {}
        self.address: int = 100
        self.build_unordered_symbol_table()
        self.build_ordered_symbol_table()


    def insert(self, name, data_type, line, scope):
        if name in self.unordered_table:
            # The Id was already added to the table just 
            # update the usage lines.
            entry = self.add_usage(name, line)
        else:
            # The Id is new and add create new object for it.
            entry = SymbolTableEntry(name, data_type, line, [line], f"0x00{self.address}", scope)
            self.address += 1
        
        # Update the Id object in the table.
        self.unordered_table[name] = entry

    
    def add_usage(self, name, line):
        entry = self.unordered_table[name]
        entry.add_usage_line(line)
        return entry

    
    def build_unordered_symbol_table(self):
        current_data_type = None
        current_scope = "Global"
        opened_braces = 0

        for token in self.tokens:
            if token.token_type == DATA_TYPE:
                current_data_type = token.lexeme
            elif token.token_type == ID:
                if current_data_type:
                    self.insert(name=token.lexeme, data_type=current_data_type, line=token.line_number, scope=current_scope)
                    current_data_type = None
                elif token.lexeme in self.unordered_table:
                    self.insert(name=token.lexeme, data_type=None, line=token.line_number, scope=current_scope)
                else:
                    raise ValueError(f"⚠️  Data type missing for identifier <{token.lexeme}>!")
            elif token.token_type == LEFT_BRACE:
                opened_braces += 1
            elif token.token_type == RIGHT_BRACE:
                opened_braces -= 1

            if opened_braces == 0: current_scope = "Global"
            else: current_scope = "Local"


    def build_ordered_symbol_table(self):
        self.ordered_table = dict(sorted(self.unordered_table.items(), key=lambda item: item[0]))
        
        # Reset the adresses to start from 0x00100
        address_counter = 100
        for _, entry in self.ordered_table.items():
            entry.address = f"0x00{address_counter}"
            address_counter += 1


    def get_unordered_symbol_table(self):
        return self.unordered_table


    def get_ordered_symbol_table(self):
        return self.ordered_table

