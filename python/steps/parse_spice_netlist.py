import re


def parse_spice_netlist(netlist):
    components = {
        "resistors": {},
        "capacitors": {},
        "inductors": {},
        "voltage_sources": {},
        "current_sources": {},
        "dependent_sources": {},
    }
    nodes = set()
    components_set = set()

    lines = netlist.split("\n")

    for line in lines:
        line = line.strip()
        if line and not line.startswith("*"):
            parts = re.split(r"\s+", line)

            component = parts[0]
            components_set.add(component)

            component_nodes = parts[1:-1]
            nodes.update(component_nodes)

            value = parts[-1]

            if component.startswith("R"):
                components["resistors"].update(
                    {component: {"value": value, "nodes": component_nodes}}
                )
            elif component.startswith("C"):
                components["capacitors"].update(
                    {component: {"value": value, "nodes": component_nodes}}
                )
            elif component.startswith("L"):
                components["inductors"].update(
                    {component: {"value": value, "nodes": component_nodes}}
                )
            elif component.startswith("V"):
                if "*" in value:
                    components["dependent_sources"].update(
                        {component: {"value": value, "nodes": component_nodes}}
                    )
                else:
                    components["voltage_sources"].update(
                        {component: {"value": value, "nodes": component_nodes}}
                    )
            elif component.startswith("I"):
                if "*" in value:
                    components["dependent_sources"].update(
                        {component: {"value": value, "nodes": component_nodes}}
                    )
                else:
                    components["current_sources"].update(
                        {component: {"value": value, "nodes": component_nodes}}
                    )

    return components, components_set, nodes
