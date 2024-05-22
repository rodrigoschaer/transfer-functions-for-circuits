from sympy import Eq, simplify, linsolve, symbols
from sympy.abc import s

R1, R2, C1, C2 = symbols('R1 R2 C1 C2', positive=True)
V1, V2, V3, Vin = symbols('V1 V2 V3 Vin')

eq1 = Eq(V1 , Vin)
eq2 = Eq(V1 * (-s * C1) + V2 * (s*C1 + 1/R1 + 1/R2) + V3 * (-1/R2), 0)
eq3 = Eq(V1*0 + V2*(-1/R2) + V3*(1/R2 + s*C2), 0)

system_solution = linsolve([eq1, eq2, eq3], (V1, V2))
print(system_solution)

print(type(system_solution))

H = simplify(system_solution[V2]/system_solution[V1])

print('Transfer Function: H(s) =', H)
