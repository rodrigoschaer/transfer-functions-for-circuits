import sympy as sp


def current_through_resistor(v1, v2, resistance):
    return (v1 - v2) / resistance


def current_through_capacitor(v1, v2, capacitance, s):
    return s * capacitance * (v1 - v2)


def current_through_inductor(v1, v2, inductance, s):
    return (v1 - v2) / (s * inductance)


def write_kcl_equations(node_connections, node_voltages, symbols):
    s = sp.symbols("s")
    kcl_equations = {}
    for node, connections in node_connections.items():
        if node == "0":
            continue

        node_current = 0
        for comp_name, comp_nodes, _ in connections:
            if comp_name.startswith("R"):
                # Resistor
                contribution = current_through_resistor(
                    node_voltages[comp_nodes[0]],
                    node_voltages[comp_nodes[1]],
                    symbols[comp_name],
                )
                node_current += contribution if comp_nodes[0] == node else -contribution

            elif comp_name.startswith("C"):
                # Capacitor
                contribution = current_through_capacitor(
                    node_voltages[comp_nodes[0]],
                    node_voltages[comp_nodes[1]],
                    symbols[comp_name],
                    s,
                )
                node_current += contribution
            elif comp_name.startswith("L"):
                # Inductor
                contribution = current_through_inductor(
                    node_voltages[comp_nodes[0]],
                    node_voltages[comp_nodes[1]],
                    symbols[comp_name],
                    s,
                )
                node_current += contribution if comp_nodes[0] == node else -contribution
            elif comp_name.startswith("V"):
                # Independent voltage source
                pass
            elif comp_name.startswith("I"):
                # Independent current source
                if comp_nodes[0] == node:
                    node_current += symbols[comp_name]
                else:
                    node_current -= (
                        symbols[comp_name]
                        if comp_name in symbols
                        else sp.symbols(comp_name)
                    )

        if node_current != 0:
            kcl_equations[node] = sp.Eq(node_current, 0)
        else:
            kcl_equations[node] = sp.Eq(node_voltages[node], 0)

    return kcl_equations
