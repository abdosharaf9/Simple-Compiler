# Initialize grammar rules
grammar = {
    'program': ['stmt_list'],
    'stmt_list': ['stmt stmt_list', 'ε'],
    'stmt': ['assign_stmt', 'print_stmt'],
    'print_stmt': ['PRINT L_PAREN ID R_PAREN SEMICOLON'],
    'assign_stmt': ['ID ASSIGN expr SEMICOLON'],
    'expr': ['term expr_tail'],
    'expr_tail': ['ARITHMETIC_OPERATOR term expr_tail', 'ε'],
    'term': ['ID', 'INT', 'FLOAT', 'L_PAREN expr R_PAREN']
}

# Initialize First and Follow sets
first_sets = {non_terminal: set() for non_terminal in grammar}
follow_sets = {non_terminal: set() for non_terminal in grammar}

# Add terminal symbols to First sets
terminals = {'ID', 'INT', 'FLOAT', 'L_PAREN', 'R_PAREN', 'ARITHMETIC_OPERATOR', 'SEMICOLON', 'PRINT'}
for terminal in terminals:
    first_sets[terminal] = {terminal}

# Initialize Follow set of start symbol
follow_sets['program'].add('$')

# Calculate First sets
def calculate_first_sets():
    changed = True
    while changed:
        changed = False
        for non_terminal, productions in grammar.items():
            for production in productions:
                symbols = production.split()
                first_symbol = symbols[0]
                if first_symbol in terminals:
                    if first_symbol not in first_sets[non_terminal]:
                        first_sets[non_terminal].add(first_symbol)
                        changed = True
                else:
                    for symbol in symbols:
                        if 'ε' not in first_sets[symbol]:
                            first_sets[non_terminal].update(first_sets[symbol])
                            if 'ε' not in first_sets[symbol]:
                                break
                    else:
                        if 'ε' not in first_sets[non_terminal]:
                            first_sets[non_terminal].add('ε')
                            changed = True

# Calculate Follow sets
def calculate_follow_sets():
    changed = True
    while changed:
        changed = False
        for non_terminal, productions in grammar.items():
            for production in productions:
                symbols = production.split()
                for i, symbol in enumerate(symbols):
                    if symbol in grammar:
                        if i < len(symbols) - 1:
                            next_symbol = symbols[i + 1]
                            if next_symbol in terminals:
                                if next_symbol not in follow_sets[symbol]:
                                    follow_sets[symbol].add(next_symbol)
                                    changed = True
                            else:
                                for first in first_sets[next_symbol]:
                                    if first != 'ε' and first not in follow_sets[symbol]:
                                        follow_sets[symbol].add(first)
                                        changed = True
                                if 'ε' in first_sets[next_symbol] and i == len(symbols) - 2:
                                    for follow in follow_sets[non_terminal]:
                                        if follow not in follow_sets[symbol]:
                                            follow_sets[symbol].add(follow)
                                            changed = True
                        else:
                            for follow in follow_sets[non_terminal]:
                                if follow not in follow_sets[symbol]:
                                    follow_sets[symbol].add(follow)
                                    changed = True

# Perform iterations to calculate stable First and Follow sets
calculate_first_sets()
calculate_follow_sets()

# Print the calculated First and Follow sets
print("First Sets:")
for non_terminal, first_set in first_sets.items():
    print(f"First({non_terminal}): {first_set}")

print("\nFollow Sets:")
for non_terminal, follow_set in follow_sets.items():
    print(f"Follow({non_terminal}): {follow_set}")
