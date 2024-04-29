from lark import Lark

grammar = """
    ?start: statement+
    ?statement: assign_stmt
    ?assign_stmt: NAME "=" expr ";"
    ?expr: term
    ?term: NUMBER
    %import common.CNAME -> NAME
    %import common.NUMBER
    %import common.WS
    %ignore WS
    """

lark_parser = Lark(grammar)

code = """
x = 55;
y = 12.5;
"""

print(lark_parser.parse(code))