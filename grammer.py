# stmt -> type id assign value | expr
# expr -> expr + expr
#         | expr - expr
#         | expr * expr
#         | expr / expr
#         | (expr)
#         | id
#         | value
# type -> int | float
# value -> num | expr
# assign -> =
# arth_opr -> + | - | * | /
# id -> r"[a-zA-Z_][a-zA-Z0-9_]*"
# num -> r"\d+(\.\d+)?"
