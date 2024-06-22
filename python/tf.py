import re
import sympy as sp

netlist = """
Vcc N001 0 DC 12
Rpi B E Rpi
beta_ib C E beta*Ib
Rc C 0 Rc
Re E 0 Re
C1 B N002 C1
C2 N002 0 C2
"""

netlist = """
* Common-Emitter Amplifier Example
Vcc N001 0 DC 12
Rpi B E Rpi
beta_ib C E beta*Ib
Rc C 0 Rc
Re E 0 Re
C1 B N002 C1
C2 N002 0 C2
E1 N003 0 N001 N002 E1_gain  ; VCVS: Vout = E1_gain * (V(N001) - V(N002))
G1 N004 0 N001 N002 G1_gain  ; VCCS: Iout = G1_gain * V(N001, N002)
F1 N005 0 V1 F1_gain         ; CCCS: Iout = F1_gain * I(V1)
H1 N006 0 V1 H1_gain         ; CCVS: Vout = H1_gain * I(V1)
"""

# Step 1: parse the input
def parse_spice(netlist):
    components = {
        'resistors': [],
        'capacitors': [],
        'inductors': [],
        'voltage_sources': [],
        'current_sources': [],
        'dependent_sources': []
    }

    lines = netlist.split('\n')

    for line in lines:
        line = line.strip()
        if line and not line.startswith('*'):
            parts = re.split(r'\s+', line)
            component = parts[0]
            nodes = parts[1:-1]
            value = parts[-1]

            if component.startswith('R'):
                components['resistors'].append((component, nodes, value))
            elif component.startswith('C'):
                components['capacitors'].append((component, nodes, value))
            elif component.startswith('L'):
                components['inductors'].append((component, nodes, value))
            elif component.startswith('V'):
                components['voltage_sources'].append((component, nodes, value))
            elif component.startswith('I'):
                components['current_sources'].append((component, nodes, value))
            elif component.startswith('E') or component.startswith('F') or component.startswith('G') or component.startswith('H'):
                components['dependent_sources'].append((component, nodes, value))
    return components

components = parse_spice(netlist)
print(f"\nStep 1: Parse spice components:")
for comp_type, comp_list in components.items():
    print(f"{comp_type}: {comp_list}")

# Step 2: Create symbolic variables
def create_sympy_symbols(components):
    symbols = {}
    for comp_type, comp_list in components.items():
        for comp in comp_list:
            name, nodes, value = comp
            if comp_type == 'resistors' or comp_type == 'capacitors' or comp_type == 'inductors':
                symbols[name] = sp.symbols(value)
            elif comp_type == 'dependent_sources':
                # Extract gain for dependent sources
                gain = value.split('*')[0]
                symbols[name] = sp.symbols(gain)
    return symbols

symbols = create_sympy_symbols(components)
print(f"\nStep 2: Create Sympy Component Symbols")
for name, symbol in symbols.items():
    print(f"{name}: {symbol}")

# Step 3: Identify Nodes
def parse_spice_netlist_with_nodes(netlist):
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
                components['voltage_sources'].append((component, component_nodes, value))
            elif component.startswith('I'):
                components['current_sources'].append((component, component_nodes, value))
            elif component.startswith('E') or component.startswith('F') or component.startswith('G') or component.startswith('H'):
                components['dependent_sources'].append((component, component_nodes, value))

    return components, nodes

components, nodes = parse_spice_netlist_with_nodes(netlist)
symbols = create_sympy_symbols(components)

for comp_type, comp_list in components.items():
    print(f"{comp_type}: {comp_list}")

print("\nStep 3: Identify Nodes:")
print(nodes)

# Step 4: Create node voltages
def create_node_voltages(nodes):
    node_voltages = {}
    for node in nodes:
        if node != '0':  # Ground node
            node_voltages[node] = sp.symbols(f'V_{node}')
        if node == '0':
            node_voltages['0'] = 0
    return node_voltages

node_voltages = create_node_voltages(nodes)
print("\n Step 4: Create Node Voltages:")
for node, voltage in node_voltages.items():
    print(f"{node}: {voltage}")

# Step 5.1: Components through nodes
def get_node_connections(components):
    node_connections = {node: [] for node in nodes}
    for comp_type, comp_list in components.items():
        for comp in comp_list:
            name, comp_nodes, value = comp
            for node in comp_nodes:
                if node in node_connections:
                    node_connections[node].append((name, comp_nodes, value))
    return node_connections

node_connections = get_node_connections(components)
print("\nStep 5: Node Connections:")
for node, connections in node_connections.items():
    print(f"{node}: {connections}")

# Step 5.2: Get nodes expressions
def current_through_resistor(v1, v2, resistance):
    return (v1 - v2) / resistance

def current_through_capacitor(v1, v2, capacitance, s):
    return s * capacitance * (v1 - v2)

def current_through_inductor(v1, v2, inductance, s):
    return (v1 - v2) / (s * inductance)

def current_through_vcvs(v_control1, v_control2, gain):
    print("VCVS | ", "V1: ", v_control1, "V2: ", v_control2)
    return gain * (v_control1 - v_control2)

def current_through_vccs(v_control1, v_control2, gain):
    return gain * (v_control1 - v_control2)

def current_through_cccs(current_control, gain):
    return gain * current_control

def voltage_through_ccvs(current_control, gain):
    return gain * current_control


# Step 6: KCL equations
def write_kcl_equations(node_connections, node_voltages, _, s):
    kcl_equations = []
    for node, connections in node_connections.items():
        if node == '0':  # Skip ground node
            continue

        current_sum = 0
        for name, comp_nodes, value in connections:
            if name.startswith('R'):
                # Resistor
                if comp_nodes[0] == node:
                    current_sum += current_through_resistor(node_voltages[node], node_voltages[comp_nodes[1]], symbols[name])
                else:
                    current_sum += current_through_resistor(node_voltages[comp_nodes[1]], node_voltages[node], symbols[name])
            elif name.startswith('C'):
                # Capacitor
                if comp_nodes[0] == node:
                    current_sum += current_through_capacitor(node_voltages[node], node_voltages[comp_nodes[1]], symbols[name], s)
                else:
                    current_sum += current_through_capacitor(node_voltages[comp_nodes[1]], node_voltages[node], symbols[name], s)
            elif name.startswith('L'):
                # Inductor
                if comp_nodes[0] == node:
                    current_sum += current_through_inductor(node_voltages[node], node_voltages[comp_nodes[1]], symbols[name], s)
                else:
                    current_sum += current_through_inductor(node_voltages[comp_nodes[1]], node_voltages[node], symbols[name], s)
            elif name.startswith('V'):
                # Independent voltage source (current is zero in the small-signal model)
                pass
            elif name.startswith('I'):
                # Independent current source
                if comp_nodes[0] == node:
                    current_sum += symbols[name]
                else:
                    current_sum -= symbols[name]
            # Handle dependent sources similarly
            elif name.startswith('E'):
                # Voltage-Controlled Voltage Source (VCVS)
                v_control1 = node_voltages[comp_nodes[2]]
                v_control2 = node_voltages[comp_nodes[3]]
                current_sum += current_through_vcvs(v_control1, v_control2, symbols[name])
            elif name.startswith('G'):
                # Voltage-Controlled Current Source (VCCS)
                v_control1 = node_voltages[comp_nodes[2]]
                v_control2 = node_voltages[comp_nodes[3]]
                current_sum += current_through_vccs(v_control1, v_control2, symbols[name])
            elif name.startswith('F'):
                # Current-Controlled Current Source (CCCS)
                # Assuming current control is specified in the value part, like "V1" (voltage source name)
                current_control = symbols[value]
                current_sum += current_through_cccs(current_control, symbols[name])
            elif name.startswith('H'):
                # Current-Controlled Voltage Source (CCVS)
                # Assuming current control is specified in the value part, like "V1" (voltage source name)
                current_control = symbols[value]
                current_sum += voltage_through_ccvs(current_control, symbols[name])
            print("Current sum: ", current_sum, "\n")
        if current_sum != 0:
            kcl_equations.append({str(node_voltages[node]): sp.Eq(current_sum, 0)})
    
    return kcl_equations

# Generate the KCL equations
kcl_equations = write_kcl_equations(node_connections, node_voltages, components, sp.symbols('s'))
print("\n Step 6: KCL Equations:")
for eq in kcl_equations:
    sp.pprint(eq)
print("Recalling nodes: ", node_voltages)