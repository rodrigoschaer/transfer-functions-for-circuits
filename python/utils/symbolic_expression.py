import sympy as sp
import re


def symbolic_expression(expression):
    expression = expression.strip("()")

    variables = re.findall(r"\b[A-Za-z_][A-Za-z0-9_]*\b", expression)
    symbolic_vars = {var: sp.symbols(var) for var in variables}

    symbolic_expr = expression
    for var in symbolic_vars:
        symbolic_expr = symbolic_expr.replace(var, f'symbolic_vars["{var}"]')

    symbolic_expr = eval(symbolic_expr)
    return symbolic_expr, symbolic_vars
