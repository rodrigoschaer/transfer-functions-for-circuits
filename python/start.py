from sympy import Eq, symbols, init_printing, solve
from sympy.abc import s
init_printing(use_unicode=True)


R1, R2, C1, C2 = symbols('R1 R2 C1 C2', positive=True)
V1, V2, I1, I2, Vout = symbols('V1 V2 I1 I2 Vout')

eq1 = Eq(s*(C1+C2)*V1 + (1/R1 + s*C1)*I1 - s*C2*V2, 0)
eq2 = Eq(-s*C2*V1 + (1/R2 + s*C2)*I2 + V2/(R2*s), 0)
eq3 = Eq(Vout/R2, I2)

sol = solve([eq1, eq2, eq3], [Vout, I1])

print(sol)
