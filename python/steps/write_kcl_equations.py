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
