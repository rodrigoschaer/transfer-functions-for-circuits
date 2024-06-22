from collections import defaultdict
import sympy as sp
from assets.netlist import NETLIST
from steps.create_node_connections import create_node_connections
from steps.create_node_voltages import create_node_voltages
from steps.create_sympy_symbols import create_sympy_symbols
from steps.parse_spice_netlist import parse_spice_netlist
from steps.write_kcl_equations import write_kcl_equations


# Step 1: Parse the input component-wise and node-
components, nodes = parse_spice_netlist(NETLIST)

# Step 2: Create symbolic variables
symbols = create_sympy_symbols(components)

# Step 3: Create node voltages symbolic variables
node_voltages, voltage_source_currents = create_node_voltages(nodes, components)

# Step 4: Components connections through nodes
node_connections = create_node_connections(components, nodes)

# Step 5: KCL equations
kcl_equations = write_kcl_equations(node_connections, node_voltages, sp.symbols('s'), symbols)

print("\nKCL Equations:")
for eq in kcl_equations.values():
    sp.pprint(eq)