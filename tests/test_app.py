import os
import sys

# Ensure the app directory is in the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import unittest
from app.app import app, load_model

class TestApp(unittest.TestCase):
    def test_load_model(self):
        """ Ensure the model loads correctly in application """
        model = load_model()
        self.assertIsNotNone(model, "Model should be loaded successfully")

    def test_post_predict(self):
        """ Test the /predict endpoint with a sample payload """

        with app.test_client() as client:
            # Ensure the app is ready to handle requests
            response = client.get('/health')
            self.assertEqual(response.status_code, 200, "Health check should return 200 OK")

            # Prepare a sample payload for prediction
            payload = {
                "X1 transaction date": 2025.10,
                "X2 house age": 10,
                "X3 distance to the nearest MRT station": 500,
                "X4 number of convenience stores": 5,
                "X5 latitude": 1.3521,
                "X6 longitude": 103.8198
            }

            # Make a POST request to the /predict endpoint
            response = client.post('/predict', json=payload)
            self.assertEqual(response.status_code, 200, "Prediction request should return 200 OK")
            self.assertIn("prediction", response.json, "Response should contain a prediction key")

if __name__ == '__main__':
    unittest.main()