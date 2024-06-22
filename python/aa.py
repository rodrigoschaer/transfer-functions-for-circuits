import re
import sympy as sp

def parse_spice_netlist_with_nodes(netlist):
    components = {
        'resistors': [],
        'capacitors': [],
        'inductors': [],
        'voltage_sources': [],
        'current_sources': [],
        'dependent_sources': []
    }
    nodes = set()

    lines = netlist.split('\n')
    
    for line in lines:
        line = line.strip()
        if line and not line.startswith('*'):
            parts = re.split(r'\s+', line)
            component = parts[0]
            component_nodes = parts[1:-1]
            value = parts[-1]
            
            nodes.update(component_nodes)  # Add nodes to the set
            
            if component.startswith('R'):
                components['resistors'].append((component, component_nodes, value))
            elif component.startswith('C'):
                components['capacitors'].append((component, component_nodes, value))
            elif component.startswith('L'):
                components['inductors'].append((component, component_nodes, value))
            elif component.startswith('V'):
                components['voltage_sources'].append((component, component_nodes, value))
            elif component.startswith('I'):
                components['current_sources'].append((component, component_nodes, value))
            elif component.startswith('E') or component.startswith('G') or component.startswith('F') or component.startswith('H'):
                components['dependent_sources'].append((component, component_nodes, value))
    
    return components, nodes

# Example netlist
netlist = """
* Common-Emitter Amplifier Example
Vcc N001 0 DC 12
Rpi B E Rpi
beta_ib C E beta*Ib
Rc C 0 Rc
Re E 0 Re
C1 B N002 C1
C2 N002 0 C2
E1 N003 0 N001 N002 E1_gain  ; VCVS: Vout = E1_gain * (V(N001) - V(N002))
G1 N004 0 N001 N002 G1_gain  ; VCCS: Iout = G1_gain * V(N001, N002)
F1 N005 0 V1 F1_gain         ; CCCS: Iout = F1_gain * I(V1)
H1 N006 0 V1 H1_gain         ; CCVS: Vout = H1_gain * I(V1)
"""

components, nodes = parse_spice_netlist_with_nodes(netlist)
print("Components:")
for comp_type, comp_list in components.items():
    print(f"{comp_type}: {comp_list}")

print("\nNodes:")
print(nodes)