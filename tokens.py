# Predefined token types that will be in my language.
TOKEN_TYPES = {
    "KEYWORD": r"(if|else|while|for|return|fun|print|when|is)\b",
    "DATA_TYPE": r"(int|float|char|string|double|short)\b",
    "ARITHMETIC_OPERATOR": r"\+|\-|\*|\/|\%",
    "RELATIONAL_OPERATOR": r"<=|>=|<|>|==|!=",
    "LOGICAL_OPERATOR": r"and|not|or",
    "BOOLEAN": r"true|false",
    "ID": r"[a-zA-Z_][a-zA-Z0-9_]*",
    "PAREN": r"\(|\)|\[|\]|\{|\}",
    "STRING": r"\"(?:\\.|[^\"\\])*\"",
    "CHAR_LITERAL": r"\'(?:\\.|[^\'])*\'",
    "NUMBER": r"\d+(\.\d+)?",
    "ASSIGN": r"\=",
    "SYMBOL": r"\;|\,|\:",
    "NEWLINE": r"\n",
    "WHITESPACE": r"\s+",
    "COMMENT": r"#[^#]*"    
}

KEYWORD = "Keyword"
ARITHMETIC_OPERATOR = "Arithmetic Operator"
RELATIONAL_OPERATOR = "Relational Operator"
ID = "ID"
INT = "Integer"
FLOAT = "Float"
ASSIGN = "Assign"
SIMI_COLON = "Simi Colon"
NEWLINE = "New line"
WHITESPACE = "Whitespace"
COMMENT = "Comment"
LEFT_PAREN = "Left Paren"
RIGHT_PAREN = "Right Paren"
EOF = "EOF"

TOKENS = {
    KEYWORD: r"(if|print)\b",
    ARITHMETIC_OPERATOR: r"\+|\-|\*|\/|\%",
    RELATIONAL_OPERATOR: r"<=|>=|<|>|==|!=",
    INT: r"\d+",
    FLOAT: r"\d+(\.\d+)?",
    ID: r"[a-zA-Z_][a-zA-Z0-9_]*",
    LEFT_PAREN: r"\(",
    RIGHT_PAREN: r"\)",
    ASSIGN: r"\=",
    SIMI_COLON: r"\;",
    COMMENT: r"#[^#]*"
}