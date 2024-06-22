import sympy as sp

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