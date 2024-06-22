def create_node_connections(components):
    node_connections = {node: [] for node in nodes}
    for comp_type, components_list in components.items():
        for comp in components_list:
            name, comp_nodes, value = comp
            for node in comp_nodes:
                if node in node_connections:
                    node_connections[node].append((name, comp_nodes, value))
    return node_connections