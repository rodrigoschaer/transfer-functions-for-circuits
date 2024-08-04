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
