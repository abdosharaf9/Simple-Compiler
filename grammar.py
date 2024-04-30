# program -> stmt_list
# stmt_list -> stmt stmt_list | ε
# stmt -> dec_stmt | assign_stmt | print_stmt | if_stmt
# dec_stmt -> DATA_TYPE assign_stmt | DATA_TYPE ID SEMICOLON
# assign_stmt -> ID ASSIGN expr SEMICOLON
# print_stmt -> PRINT LEFT_PAREN ID RIGHT_PAREN SEMICOLON
# if_stmt -> IF LEFT_PAREN rel_expr RIGHT_PAREN LEFT_BRACE stmt RIGHT_BRACE
# expr -> term arth_expr
# arth_expr -> ARITHMETIC_OPERATOR term arth_expr | ε
# rel_expr -> arth_expr RELATIONAL_OPERATOR arth_expr
# term -> ID | NUMBER | LEFT_PAREN expr RIGHT_PAREN
