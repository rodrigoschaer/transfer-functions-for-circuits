import unittest
from circuit_model import CircuitModel
from sympy import symbols

class CircuitModelTests(unittest.TestCase):
    def test_create_symbolic_variable(self):
        # Test the create_symbolic_variable method of the CircuitModel class
        circuit_model = CircuitModel(num_nodes=4)
        symbol = circuit_model.create_symbolic_variable("resistor", node1=1, node2=2)
        self.assertIsNotNone(symbol)

    def test_create_equation(self):
        # Test the create_equation method of the CircuitModel class
        circuit_model = CircuitModel(num_nodes=4)
        equation = circuit_model.create_equation("resistor", node1=1, node2=2, symbol=symbols('R_symbol_1_2'))
        self.assertIsNotNone(equation)

if __name__ == '__main__':
    unittest.main()
