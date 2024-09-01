import re

import sympy as sp


def calculate_transfer_function(netlist):

    # Step 0: define reference for laplace variable
    s = sp.symbols("s")

    # Step 1: Parse the input component-wise and node-wise
    components, nodes = parse_spice_netlist(netlist)

    # Step 2: Create node voltages symbolic variables
    node_symbols = create_node_symbols(nodes)

    # Step 3: Create symbolic variables
    component_symbols = create_component_symbols(components, node_symbols, nodes)

    # Step 4: Components connections through nodes
    node_connections = create_nodes_to_components_connections(components, nodes)

    # Step 5: KCL equations
    kcl_equations = write_kcl_equations(node_connections, node_symbols, component_symbols, s)

    # Step 6: calculate the transfer function
    tf = calculate_tf_from_kcl(
        kcl_equations, node_symbols["V_IN"], node_symbols["V_OUT"], node_symbols, s
    )
    return tf, kcl_equations


def parse_spice_netlist(netlist):
    components = {
        "resistors": {},
        "capacitors": {},
        "inductors": {},
        "independent_sources": {},
        "dependent_sources": {},
    }
    nodes = set()

    lines = netlist.split("\n")
    for line in lines:
        line = line.strip()
        if line and not line.startswith("*"):
            parts = re.split(r"\s+", line)
            component = parts[0]

            if component.startswith("R"):
                component_nodes = [parts[1], parts[2]]
                nodes.update(component_nodes)
                value = parts[-1]

                components["resistors"].update(
                    {component: {"value": value, "nodes": component_nodes}}
                )
            elif component.startswith("C"):
                component_nodes = [parts[1], parts[2]]
                nodes.update(component_nodes)
                value = parts[-1]

                components["capacitors"].update(
                    {component: {"value": value, "nodes": component_nodes}}
                )
            elif component.startswith("L"):
                component_nodes = [parts[1], parts[2]]
                nodes.update(component_nodes)
                value = parts[-1]

                components["inductors"].update(
                    {component: {"value": value, "nodes": component_nodes}}
                )
            elif component.startswith("V") or component.startswith("I"):
                component_nodes = [parts[1], parts[2]]
                nodes.update(component_nodes)
                value = parts[-1]

                components["independent_sources"].update(
                    {component: {"value": value, "nodes": component_nodes}}
                )
            elif component.startswith("E") or component.startswith("G"):
                # G1 V- V+ dp+ dp- G
                component_nodes = [parts[1], parts[2]]
                nodes.update(component_nodes)
                dependency = (parts[3], parts[4])
                gain = parts[-1]

                components["dependent_sources"].update(
                    {component: {"value": gain, "nodes": component_nodes, "dependency": dependency}}
                )

    return components, nodes


def create_node_symbols(nodes):
    def parse_symbolic_expression(expression):
        expression = expression.strip("()")

        variables = re.findall(r"\b[A-Za-z_][A-Za-z0-9_]*\b", expression)
        symbolic_vars = {var: sp.symbols(var) for var in variables}

        symbolic_expr = expression
        for var in symbolic_vars:
            symbolic_expr = symbolic_expr.replace(var, f'symbolic_vars["{var}"]')

        symbolic_expr = eval(symbolic_expr)
        return symbolic_expr, symbolic_vars

    node_symbols = {}

    node_symbols["0"] = 0
    for node in nodes:
        if node != "0":
            symbolic_expr, symbolic_vars = parse_symbolic_expression(node)
            node_symbols[node] = symbolic_expr

            for var in symbolic_vars:
                node_symbols[var] = sp.symbols(var)

    return node_symbols


def create_component_symbols(components, node_symbols, nodes):
    component_symbols = {}
    toIgnore = []

    for component_type in components:
        if component_type in toIgnore:
            continue

        components_list = components[component_type]
        for component_name in components_list:
            if component_type in ["resistors", "capacitors", "inductors"]:
                component_symbols[component_name] = sp.symbols(component_name)

            elif component_type == "dependent_sources":
                gain = sp.symbols(components_list[component_name]["value"])

                dependency_nodes = components_list[component_name]["dependency"]
                start, end = dependency_nodes

                if start not in node_symbols or end not in node_symbols:
                    raise Exception(
                        "Failed to parse dependent source. The provided nodes were not found in the circuit."
                    )

                dependent_source_expression = gain * (node_symbols[start] - node_symbols[end])
                component_symbols[component_name] = dependent_source_expression

    return component_symbols


def create_nodes_to_components_connections(components, nodes):
    node_connections = {node: [] for node in nodes}
    for component_type in components:
        components_list = components[component_type]
        for component_name in components_list:
            component_nodes = components_list[component_name]["nodes"]
            component_value = components_list[component_name]["value"]
            for node in component_nodes:
                if node in node_connections:
                    node_connections[node].append(
                        (component_name, component_nodes, component_value)
                    )
    return node_connections


def write_kcl_equations(node_connections, node_voltages, symbols, s):
    def current_through_resistor(v1, v2, resistance):
        return (v1 - v2) / resistance

    def current_through_capacitor(v1, v2, capacitance, s):
        return s * capacitance * (v1 - v2)

    def current_through_inductor(v1, v2, inductance, s):
        return 1 / (s * inductance) * (v1 - v2)

    kcl_equations = {}
    for node, connections in node_connections.items():
        if node == "0":
            continue

        node_current = 0
        for comp_name, comp_nodes, _ in connections:
            if comp_name.startswith("R"):
                node_current += (
                    current_through_resistor(
                        node_voltages[comp_nodes[0]],
                        node_voltages[comp_nodes[1]],
                        symbols[comp_name],
                    )
                    if comp_nodes[0] == node
                    else current_through_resistor(
                        node_voltages[comp_nodes[1]],
                        node_voltages[comp_nodes[0]],
                        symbols[comp_name],
                    )
                )

            elif comp_name.startswith("C"):
                node_current += (
                    current_through_capacitor(
                        node_voltages[comp_nodes[0]],
                        node_voltages[comp_nodes[1]],
                        symbols[comp_name],
                        s,
                    )
                    if comp_nodes[0] == node
                    else current_through_capacitor(
                        node_voltages[comp_nodes[1]],
                        node_voltages[comp_nodes[0]],
                        symbols[comp_name],
                        s,
                    )
                )

            elif comp_name.startswith("L"):
                node_current += (
                    current_through_inductor(
                        node_voltages[comp_nodes[0]],
                        node_voltages[comp_nodes[1]],
                        symbols[comp_name],
                        s,
                    )
                    if comp_nodes[0] == node
                    else current_through_inductor(
                        node_voltages[comp_nodes[1]],
                        node_voltages[comp_nodes[0]],
                        symbols[comp_name],
                        s,
                    )
                )
            elif comp_name.startswith("I") or comp_name.startswith("G"):
                if comp_nodes[0] == node:
                    node_current += (
                        symbols[comp_name] if comp_name in symbols else sp.symbols(comp_name)
                    )
                else:
                    node_current -= (
                        symbols[comp_name] if comp_name in symbols else sp.symbols(comp_name)
                    )
            elif comp_name.startswith("V") or comp_name.startswith("E"):
                # Independent voltage source will be treated as a current source of equal contribution
                if comp_nodes[0] == node:
                    node_current += (
                        symbols[comp_name] if comp_name in symbols else sp.symbols(comp_name)
                    )
                else:
                    node_current -= (
                        symbols[comp_name] if comp_name in symbols else sp.symbols(comp_name)
                    )

        if node_current != 0:
            kcl_equations[node] = sp.Eq(node_current, 0)
        else:
            kcl_equations[node] = sp.Eq(node_voltages[node], 0)

    return kcl_equations


def normalize_transfer_function(tf, s):
    rationalized_tf = tf.ratsimp().collect(s)
    numerator, denominator = sp.fraction(rationalized_tf)

    leading_coeff = sp.LC(denominator, s)
    numerator_normalized = (numerator / leading_coeff).collect(s)
    denominator_normalized = (denominator / leading_coeff).collect(s)

    numerator_normalized = sp.collect(sp.expand(numerator_normalized), s)
    denominator_normalized = sp.collect(sp.expand(denominator_normalized), s)

    return numerator_normalized, denominator_normalized


def calculate_tf_from_kcl(kcl_equations, input, output, node_symbols, s):
    eq_list = list([value for key, value in kcl_equations.items() if "V_IN" not in key])
    solutions = sp.solve(eq_list, {"V_OUT": node_symbols["V_OUT"], "V_IN": node_symbols["V_IN"]})
    transfer_function = sp.simplify(solutions[output] / solutions[input])
    numerator, denominator = normalize_transfer_function(transfer_function, s)

    H_s = sp.Mul(numerator, sp.Pow(denominator, -1), evaluate=False)

    return H_s
