from sympy import init_printing, factor, expand, symbols
init_printing(use_unicode=True)

x, y = symbols('x y')
expr = x + 2*y

expanded_expr = expand(x*expr)
print(factor(expanded_expr))
