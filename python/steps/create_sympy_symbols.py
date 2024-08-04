from collections import defaultdict
import sympy as sp

from utils.symbolic_expression import symbolic_expression


def create_component_symbols(components, node_symbols, nodes):
    component_symbols = defaultdict()
    toIgnore = ["voltage_sources"]

    for component_type in components:
        if component_type in toIgnore:
            continue

        components_list = components[component_type]
        for component_name in components_list:
            if component_type in ["resistors", "capacitors", "inductors"]:
                component_symbols[component_name] = sp.symbols(component_name)

            elif component_type == "dependent_sources":
                component_value = components_list[component_name]["value"]

                gain = component_value.split("*")[0]
                symbolic_expr, symbolic_nodes = symbolic_expression(
                    component_value.split("*")[1]
                )

                for var in symbolic_nodes:
                    if var not in nodes:
                        node_symbols[str(var)] = sp.symbols(var)

                component_symbols[component_name] = sp.symbols(gain) * (symbolic_expr)

    return component_symbols
