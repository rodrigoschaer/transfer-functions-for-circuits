from sympy import symbols, Eq, solve

class CircuitModel:
    # Inicializar as variáveis
    def __init__(self):
        self.num_nodes = 0
        self.node_voltages = ''
        self.component_currents = []
        self.component_equations = []
        self.node_equations = []
        self.all_equations = []
        self.results = {}

    # Método para criar as variáveis de circuito
    def create_symbolic_variables(self, num_nodes):
        self.num_nodes = num_nodes
        self.node_voltages = [symbols(f'V{i}') for i in range(1, num_nodes + 1)]
        self.component_currents = [symbols(f'I{i}') for i in range(1, num_nodes)]

    def add_component(self, component):
        component_type = component['type']
        node1 = component['node1']
        node2 = component['node2']

        match component_type:
            case 'resistor':
                resistance = component['resistance']
                # Implementar comportamento para resistência
            
            case 'capacitor':
                capacitance = component['capacitance']
                # Implementar equação para a capacitância 
            
            case 'indepentent_source':
                source_type = component['source_type']
                # Implementar equação para fonte independente

            case 'dependent_source':
                source_type = component['source_type']
                # Implementar equação para fonte dependente  

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
