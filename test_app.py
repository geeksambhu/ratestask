import unittest
import requests

class TestRatesAPI(unittest.TestCase):
    def setUp(self):
        # Set the base URL for the API
        self.base_url = "http://localhost:1300"

    def test_get_rates(self):
        # Set the URL and parameters for the request
        url = self.base_url + "/rates"
        params = {
            "date_from": "2016-01-01",
            "date_to": "2016-01-10",
            "origin": "CNSGH",
            "destination": "north_europe_main"
        }

        # Send the GET request
        res = requests.get(url, params=params)

        # Check the status code
        self.assertEqual(res.status_code, 200)

        # Check the response data
        data = res.json()
        self.assertIsInstance(data, list)
        self.assertGreater(len(data), 0)
        for item in data:
            self.assertIsInstance(item, dict)
            self.assertIn("day", item)
            self.assertIsInstance(item["day"], str)
            self.assertIn("average_price", item)
            self.assertIsInstance(item["average_price"], int)

if __name__ == "__main__":
    unittest.main()
