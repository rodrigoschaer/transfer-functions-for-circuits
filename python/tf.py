from collections import defaultdict
import re
import sympy as sp

netlist = """
* Example Circuit
Vs V1 0 DC 0
RB V1 V2 RB
r_pi V2 V3 r_pi
I1 V3 0 DC gm*V_be
RC V3 V0 RC
"""

# Step 1: Parse the input component-wise and node-
def parse_spice_netlist(netlist):
    components = {
        'resistors': [],
        'capacitors': [],
        'inductors': [],
        'voltage_sources': [],
        'current_sources': [],
        'dependent_sources': []
    }
    nodes = set()

    lines = netlist.split('\n')
    
    for line in lines:
        line = line.strip()
        if line and not line.startswith('*'):
            parts = re.split(r'\s+', line)
            component = parts[0]
            component_nodes = parts[1:-1]
            value = parts[-1]
            
            nodes.update(component_nodes)  # Add nodes to the set
            
            if component.startswith('R'):
                components['resistors'].append((component, component_nodes, value))
            elif component.startswith('C'):
                components['capacitors'].append((component, component_nodes, value))
            elif component.startswith('L'):
                components['inductors'].append((component, component_nodes, value))
            elif component.startswith('V'):
                if '*' in value:
                    components['dependent_sources'].append((component, component_nodes, value))
                else:
                    components['voltage_sources'].append((component, component_nodes, value))
            elif component.startswith('I'):
                if '*' in value:
                    components['dependent_sources'].append((component, component_nodes, value))
                else:
                    components['current_sources'].append((component, component_nodes, value))
    
    return components, nodes
components, nodes = parse_spice_netlist(netlist)

# Step 2: Create symbolic variables
def create_sympy_symbols(components):
    symbols = {}
    
    for component_type, components_list in components.items():
        for comp in components_list:
            name, nodes, value = comp
            if component_type in ['resistors', 'capacitors', 'inductors']:
                symbols[name] = sp.symbols(value)
            elif component_type == 'dependent_sources':
                gain = value.split('*')[0]
                node = value.split('*')[1]
                symbols[name] = sp.symbols(gain) * sp.symbols(f'{str(node).upper()}')
    
    return symbols
symbols = create_sympy_symbols(components)

# Step 3: Create node voltages symbolic variables
def create_node_voltages_and_currents(nodes, components):
    node_voltages = {}
    dependent_nodes_voltage = {}

    node_voltages['0'] = 0
    for node in nodes:
        if node != '0':
            node_voltages[node] = sp.symbols(f'V_{node}')
    
    for dependent_source in components['dependent_sources']:
        _, _, value = dependent_source
        dependent_nodes = value.split('*')[1:]
        for node in dependent_nodes:
            dependent_nodes_voltage[node] = sp.symbols(f'{str(node).upper()}')
    
    return node_voltages, dependent_nodes_voltage
node_voltages, voltage_source_currents = create_node_voltages_and_currents(nodes, components)

# Step 4: Components through nodes
def get_node_connections(components):
    node_connections = {node: [] for node in nodes}
    for comp_type, components_list in components.items():
        for comp in components_list:
            name, comp_nodes, value = comp
            for node in comp_nodes:
                if node in node_connections:
                    node_connections[node].append((name, comp_nodes, value))
    return node_connections
node_connections = get_node_connections(components)

# Step 5: KCL equations
def current_through_resistor(v1, v2, resistance):
    return (v1 - v2) / resistance

def current_through_capacitor(v1, v2, capacitance, s):
    return s * capacitance * (v1 - v2)

def current_through_inductor(v1, v2, inductance, s):
    return (v1 - v2) / (s * inductance)

def write_kcl_equations(node_connections, node_voltages, s, symbols):
    kcl_equations = defaultdict()
    for node, connections in node_connections.items():
        if node == '0':  # Skip ground node
            continue
        
        node_current = 0
        for name, comp_nodes, value in connections:
            if name.startswith('R'):
                # Resistor
                if comp_nodes[0] == node:
                    node_current += current_through_resistor(node_voltages[node], node_voltages[comp_nodes[1]], symbols[name])
                else:
                    node_current += current_through_resistor(node_voltages[comp_nodes[1]], node_voltages[node], symbols[name])
            elif name.startswith('C'):
                # Capacitor
                if comp_nodes[0] == node:
                    node_current += current_through_capacitor(node_voltages[node], node_voltages[comp_nodes[1]], symbols[name], s)
                else:
                    node_current += current_through_capacitor(node_voltages[comp_nodes[1]], node_voltages[node], symbols[name], s)
            elif name.startswith('L'):
                # Inductor
                if comp_nodes[0] == node:
                    node_current += current_through_inductor(node_voltages[node], node_voltages[comp_nodes[1]], symbols[name], s)
                else:
                    node_current += current_through_inductor(node_voltages[comp_nodes[1]], node_voltages[node], symbols[name], s)
            elif name.startswith('V'):
                # Independent voltage source
                pass
            elif name.startswith('I'):
                # Independent current source
                if comp_nodes[0] == node:
                    node_current += symbols[name]
                else:
                    node_current -= symbols[name]
        
        if node_current != 0:
            kcl_equations[node] = sp.Eq(node_current, 0)
        else:
            kcl_equations[node] = sp.Eq(node_voltages[node], 0)

    return kcl_equations

kcl_equations = write_kcl_equations(node_connections, node_voltages, sp.symbols('s'), symbols)
print("\n Step 6: KCL Equations:")
for eq in kcl_equations.values():
    sp.pprint(eq)