import sympy as sp

import PySpice.Spice.BasicElement as el 
from PySpice.Spice.Parser import Circuit, SpiceParser

def parse (circuit_file: str) -> Circuit:
    parsed_circuit = SpiceParser(circuit_file)
    circuit = parsed_circuit.build_circuit()
    return circuit

def spice_component_to_sympy(component):
    if isinstance(component, el.Resistor or el.BehavioralResistor):
        return sp.symbols(component.name)
    elif isinstance(component,el.BehavioralCapacitor):
        return 1 / (sp.symbols('s') * sp.symbols(component.name))
    elif isinstance(component, el.BehavioralInductor):
        return (sp.symbols('s') * sp.symbols(component.name))
    else:
        return sp.symbols(component.name)
