import unittest
import json
from server import app

class APITestCase(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        self.client.testing = True

    def test_add_product(self):
        response = self.client.post('/products', json={'name': 'Laptop Dell'})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(json.loads(response.data)['name'], 'Laptop Dell')

    def test_get_products(self):
        response = self.client.get('/products')
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
