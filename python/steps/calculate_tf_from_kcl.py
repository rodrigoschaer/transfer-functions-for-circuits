import sympy as sp


def calculate_tf_from_kcl(kcl_equations, input, output, node_symbols):
    eq_list = list(kcl_equations.values())
    solutions = sp.solve(eq_list, node_symbols)
    transfer_function = sp.simplify(solutions[output] / solutions[input])
    return transfer_function
