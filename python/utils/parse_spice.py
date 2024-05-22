import re
import sympy as sp

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
