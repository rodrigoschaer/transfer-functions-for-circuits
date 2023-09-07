import unittest
import json
from app import app

class FlaskAppTests(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()

    def test_add_circuit_route(self):
        # Test the "Add Circuit" route
        data = {
            "num_nodes": 4,
            "components": [
                {
                    "name": "resistor",
                    "node1": 1,
                    "node2": 2
                },
                {
                    "name": "capacitor",
                    "node1": 2,
                    "node2": 3
                }
            ]
        }
        response = self.app.post('/api/add_circuit', json=data)
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['message'], 'Circuit added successfully')

    def test_get_equations_route(self):
        # Test the "Get Equations" route
        response = self.app.get('/api/get_equations')
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(response.status_code, 200)

    def test_calculate_transfer_function_route(self):
        # Test the "Calculate Transfer Function" route
        data = {
            "selected_variables": ["V1", "V2"]
        }
        response = self.app.post('/api/calculate_transfer_function', json=data)
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
