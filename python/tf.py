import sympy as sp
from assets.netlist import COMMON_EMITTER
from steps.calculate_tf_from_kcl import calculate_tf_from_kcl
from steps.create_node_connections import create_nodes_to_components_connections
from steps.create_node_voltages import create_node_symbols
from steps.create_sympy_symbols import create_component_symbols
from steps.parse_spice_netlist import parse_spice_netlist
from steps.write_kcl_equations import write_kcl_equations

# Step 1: Parse the input component-wise and node-wise
components, components_set, nodes = parse_spice_netlist(COMMON_EMITTER)


# Step 2: Create node voltages symbolic variables
node_symbols = create_node_symbols(nodes)


# Step 3: Create symbolic variables
component_symbols = create_component_symbols(components, node_symbols, nodes)


# Step 4: Components connections through nodes
node_connections = create_nodes_to_components_connections(components, nodes)


# Step 5: KCL equations
kcl_equations = write_kcl_equations(node_connections, node_symbols, component_symbols)
print("\nKCL Equations:")
for node, eq in kcl_equations.items():
    print(node)
    sp.pprint(eq)


# Step 6: calculate the transfer function
transfer_function = calculate_tf_from_kcl(
    kcl_equations, node_symbols["V_IN"], node_symbols["V_OUT"], node_symbols
)
print("\nLiteral Transfer Function:")
sp.pprint(transfer_function)
