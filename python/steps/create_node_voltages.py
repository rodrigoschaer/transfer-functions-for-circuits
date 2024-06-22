def create_node_voltages(nodes, components):
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