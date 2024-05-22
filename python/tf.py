import re
import sympy as sp

netlist = """
* Common-Emitter Amplifier Example
Vcc N001 0 DC 12
Rpi B E Rpi
beta_ib C E beta*Ib
Rc C 0 Rc
Re E 0 Re
C1 B N002 C1
C2 N002 0 C2
"""

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
for comp_type, comp_list in components.items():
    print(f"{comp_type}: {comp_list}")

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
for name, symbol in symbols.items():
    print(f"{name}: {symbol}")

