# program -> stmt_list
# stmt_list -> stmt stmt_list | ε
# stmt -> assign_stmt | print_stmt | if_stmt
# print_stmt -> PRINT LEFT_PAREN ID RIGHT_PAREN SEMICOLON
# if_stmt -> IF LEFT_PAREN rel_expr RIGHT_PAREN LEFT_BRACE stmt RIGHT_BRACE
# assign_stmt -> ID ASSIGN expr SEMICOLON
# expr -> term arth_expr
# arth_expr -> ARITHMETIC_OPERATOR term arth_expr | ε
# rel_expr -> arth_expr RELATIONAL_OPERATOR arth_expr
# term -> ID | NUMBER | LEFT_PAREN expr RIGHT_PAREN
