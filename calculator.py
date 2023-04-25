import sympy as sp


# Given a circuit of four net currents
I1, I2, I3, I4 = sp.symbols('I1 I2 I3 I4')

equation_one = sp.Eq(I1 + I2, I3) # This means I1 + I2 = I3
equation_two = sp.Eq(I2 + I4, I3)

solution = sp.solve([equation_one, equation_two], sp.symbols('V1 V2 V3'))
V1, V2, V3 = solution.values()
