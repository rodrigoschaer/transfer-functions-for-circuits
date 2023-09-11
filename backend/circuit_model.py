from sympy import symbols, Eq, solve

class CircuitModel:
    def __init__(self):
        self.num_nodes = None
        self.node_voltages = None
        self.component_currents = None
        self.component_equations = []
        self.node_equations = []
        self.all_equations = []
        self.results = {}

    def create_symbolic_variables(self, num_nodes):
        self.num_nodes = num_nodes
        self.node_voltages = [symbols(f'V{i}') for i in range(1, num_nodes + 1)]
        self.component_currents = [symbols(f'I{i}') for i in range(1, num_nodes)]

    def add_component(self, component):
        component_type = component['type']
        node1 = component['node1']
        node2 = component['node2']

        if component_type == 'resistor':
            resistance = component['resistance']
            voltage_drop = self.node_voltages[node1 - 1] - self.node_voltages[node2 - 1]
            current = voltage_drop / resistance
            self.component_equations.append(Eq(self.component_currents[node1 - 1], current))
            self.component_equations.append(Eq(self.component_currents[node2 - 1], -current))
        
        elif component_type == 'capacitor':
            capacitance = component['capacitance']
            # Implement equations for capacitors similarly
    
        elif component_type == 'independent_source':
            source_type = component['source_type']
            value = component['value']
            # Implement equations for independent sources similarly

        elif component_type == 'dependent_source':
            source_type = component['source_type']
            gain = component['gain']
            # Implement equations for dependent sources similarly

    # Add support for other component types as needed

    def apply_kcl(self):
        for i in range(self.num_nodes):
            node_currents = [self.component_currents[j] for j in range(self.num_nodes) if j != i]
            sum_currents = sum(node_currents)
            self.node_equations.append(Eq(sum_currents, 0))

    def generate_equations(self):
        self.all_equations = self.component_equations + self.node_equations

    def solve_circuit(self):
        node_voltage_solutions = solve(self.all_equations, self.node_voltages)
        self.results['node_voltages'] = {str(node): node_voltage_solutions[node] for node in self.node_voltages}

    def get_results(self):
        return self.results
