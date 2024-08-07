from collections import defaultdict

import sympy as sp


def create_node_symbols(nodes):
    node_symbols = defaultdict()

    node_symbols["0"] = 0
    for node in nodes:
        if node != "0":
            node_symbols[node] = sp.symbols(node)

    return node_symbols
