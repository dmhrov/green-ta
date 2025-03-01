import unittest
import requests
import time
import os

class TestFlaskApp(unittest.TestCase):
    def test_health_endpoint(self):
        time.sleep(30)
        

        host = os.environ.get('APP_HOST', 'localhost')
        port = os.environ.get('APP_PORT', '5000')
        url = f"http://{host}:{port}/health"
        
        response = requests.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['status'], 'healthy')

if __name__ == '__main__':
    unittest.main()