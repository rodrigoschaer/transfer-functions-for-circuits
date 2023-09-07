from flask import Flask, request, jsonify
from circuit_model import CircuitModel

app = Flask(__name__)
circuit_model = CircuitModel(num_nodes=4)  # Set the number of nodes (N) as needed

@app.route('/api/add_circuit', methods=['POST'])
def add_circuit():
    data = request.json

    # Extract circuit data from the request (e.g., number of nodes, components)
    num_nodes = data['num_nodes']
    components = data['components']

    # Initialize the CircuitModel with the number of nodes
    circuit_model = CircuitModel(num_nodes)

    # Add components to the circuit model
    for component in components:
        name = component['name']
        node1 = component['node1']
        node2 = component['node2']
        symbol = circuit_model.create_symbolic_variable(name, node1, node2)
        equation = circuit_model.create_equation(name, node1, node2, symbol)

        # Add the component to the circuit model
        circuit_model.add_component({
            'name': name,
            'symbol': symbol,
            'equation': equation
        })

    return jsonify({'message': 'Circuit added successfully'})

@app.route('/api/get_equations', methods=['GET'])
def get_equations():
    # Retrieve symbolic equations for the circuit from the circuit model
    equations = [component['equation'] for component in circuit_model.components]
    equations_str = [str(eq) for eq in equations]
    return jsonify({'equations': equations_str})

@app.route('/api/calculate_transfer_function', methods=['POST'])
def calculate_transfer_function():
    data = request.json

    # Extract user's selection of variables for the transfer function
    selected_variables = data['selected_variables']

    # Perform symbolic circuit analysis based on the selected variables
    # Calculate the transfer function and return it in literal form

    return jsonify({'transfer_function': 'G(s) = ...'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
