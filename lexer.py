import re
from tokens import *

class Lexer:
    def __init__(self, code: str) -> None:
        """Initialize the Lexer with the source code, and then loop over it.

        Args:
            code (str): Source code.
        """
        # Split the source code using a regex for more effeciency.
        self.code_slices = re.findall(r'(?:"[^"]*"|#[^\n]*|[0-9]+\.[0-9]+|\w+|<=|>=|==|!=|\S)', code)
        self.tokens = []
        self.check_tokens()
        

    def check_tokens(self) -> None:
        """Loop over the splitted source code and get the token type for
        each lexeme. Also, it handles the error when there is a lexeme
        doesn't match any type.
        """
        for slice in self.code_slices:
            match = None
            
            for token_type, pattern in TOKENS.items():
                match = re.match(pattern, slice)
                
                # Check if matched and not a comment (To remove the comments).
                if match and token_type != COMMENT:
                    self.tokens.append((slice, token_type))
                    break
                
            if not match:
                # Found a lexeme that doesn't match with any type.
                raise SyntaxError(f"⚠️  Lexical Error, unrecognized token: <{slice}>! Please follow the language rules.")
    
    
    def get_tokens(self) -> list[tuple[str, str]]:
        """Returns: list of lexemes and their token types."""
        return self.tokens

