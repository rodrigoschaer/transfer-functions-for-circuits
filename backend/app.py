from flask import Flask, request, jsonify
from circuit_model import CircuitModel

app = Flask(__name__)
# Rota para adicionar nos
# cm.add_node()

@app.route('/api/add_circuit', methods=['POST'])
def add_circuit():
    data = request.json
 
    num_nodes = data['num_nodes']
    components = data['components']
    
    # Passar o número de nós para inicializar o CM
    circuit_model = CircuitModel(num_nodes)

    for component in components:
        name = component['name']
        node1 = component['node1']
        node2 = component['node2']
        symbol = circuit_model.create_symbolic_variable(name, node1, node2)
        equation = circuit_model.create_equation(name, node1, node2, symbol)

        circuit_model.add_component({
            'name': name,
            'symbol': symbol,
            'equation': equation
        })

    return jsonify({'message': 'Circuit added successfully'})

@app.route('/api/get_equations', methods=['GET'])
def get_equations():
    # Retornar as equações salvas no circuit model
    equations = [component['equation'] for component in circuit_model.components]
    equations_str = [str(eq) for eq in equations]
    return jsonify({'equations': equations_str})

@app.route('/api/calculate_transfer_function', methods=['POST'])
def calculate_transfer_function():
    data = request.json

    # Variável de circuito escolhidas para a TF
    selected_variables = data['selected_variables']

    # TODO: adicionar aqui a resolução das equações de nó e a solução do 
    # sistema linear

    return jsonify({'transfer_function': 'G(s) = ...'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
