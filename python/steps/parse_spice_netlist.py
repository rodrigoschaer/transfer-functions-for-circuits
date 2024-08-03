import re


def parse_spice_netlist(netlist):
    components = {
        "resistors": [],
        "capacitors": [],
        "inductors": [],
        "voltage_sources": [],
        "current_sources": [],
        "dependent_sources": [],
    }
    nodes = set()

    lines = netlist.split("\n")

    for line in lines:
        line = line.strip()
        if line and not line.startswith("*"):
            parts = re.split(r"\s+", line)
            component = parts[0]
            component_nodes = parts[1:-1]
            value = parts[-1]

            nodes.update(component_nodes)

            if component.startswith("R"):
                components["resistors"].append((component, component_nodes, value))
            elif component.startswith("C"):
                components["capacitors"].append((component, component_nodes, value))
            elif component.startswith("L"):
                components["inductors"].append((component, component_nodes, value))
            elif component.startswith("V"):
                if "*" in value:
                    components["dependent_sources"].append(
                        (component, component_nodes, value)
                    )
                else:
                    components["voltage_sources"].append(
                        (component, component_nodes, value)
                    )
            elif component.startswith("I"):
                if "*" in value:
                    components["dependent_sources"].append(
                        (component, component_nodes, value)
                    )
                else:
                    components["current_sources"].append(
                        (component, component_nodes, value)
                    )

    return components, nodes
