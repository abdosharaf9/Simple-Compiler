# Constant titles.
KEYWORD = "Keyword"
ARITHMETIC_OPERATOR = "Arithmetic Operator"
RELATIONAL_OPERATOR = "Relational Operator"
NUMBER = "Number"
ID = "ID"
LEFT_PAREN = "Left Parenthesis"
RIGHT_PAREN = "Right Parenthesis"
LEFT_BRACE = "Left Brace"
RIGHT_BRACE = "Right Brace"
ASSIGN = "Assign Operator"
SEMICOLON = "Semicolon"
COMMENT = "Comment"
EOF = "EOF"


# Predefined token types that will be in my language.
TOKENS = {
    KEYWORD: r"(if|print)\b",
    ARITHMETIC_OPERATOR: r"\+|\-|\*|\/|\%",
    RELATIONAL_OPERATOR: r"<=|>=|<|>|==|!=",
    NUMBER: r"\d+(\.\d+)?",
    ID: r"[a-zA-Z_][a-zA-Z0-9_]*",
    LEFT_PAREN: r"\(",
    RIGHT_PAREN: r"\)",
    LEFT_BRACE: r"\{",
    RIGHT_BRACE: r"\}",
    ASSIGN: r"\=",
    SEMICOLON: r"\;",
    COMMENT: r"#[^#]*"
}
