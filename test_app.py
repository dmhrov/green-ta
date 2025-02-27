import unittest
import requests
import time
import os

class TestHealthEndpoint(unittest.TestCase):
    def test_health_endpoint(self):
        # Використовуємо змінну середовища для URL або за замовчуванням localhost
        base_url = os.environ.get('APP_URL', 'http://localhost:5000')
        url = f"{base_url}/health"
        
        # Додаємо затримку для того, щоб додаток встиг запуститись
        time.sleep(10)
        
        # Додаємо повторні спроби з'єднання
        max_retries = 5
        for attempt in range(max_retries):
            try:
                response = requests.get(url, timeout=5)
                self.assertEqual(response.status_code, 200)
                data = response.json()
                self.assertEqual(data["status"], "healthy")
                print("Health check passed!")
                return
            except (requests.exceptions.ConnectionError, requests.exceptions.Timeout) as e:
                if attempt < max_retries - 1:
                    print(f"Connection attempt {attempt+1} failed. Retrying in 5 seconds...")
                    time.sleep(5)
                else:
                    raise e
                    
if __name__ == '__main__':
    unittest.main()