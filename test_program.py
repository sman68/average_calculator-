import requests
import json

# Sample data to test the microservice
sample_data = {
    "data": [
        {"date": "2023-05-01 08:00:00", "amount": 250},
        {"date": "2023-05-01 12:00:00", "amount": 500},
        {"date": "2023-05-01 18:00:00", "amount": 300},
        {"date": "2023-05-02 08:00:00", "amount": 200},
        {"date": "2023-05-02 12:00:00", "amount": 400},
        {"date": "2023-05-02 18:00:00", "amount": 600},
        {"date": "2023-05-03 08:00:00", "amount": 350},
        {"date": "2023-05-03 12:00:00", "amount": 450},
        {"date": "2023-05-03 18:00:00", "amount": 550},
    ]
}

def test_microservice(url, data):
    print(f"Sending data to {url}:")
    print(json.dumps(data, indent=4))
    response = requests.post(url, json=data)
    print(f"Response status code: {response.status_code}")
    if response.status_code == 200:
        print("Response data:")
        print(json.dumps(response.json(), indent=4))
    else:
        print(f"Error: {response.text}")

if __name__ == '__main__':
    base_url = 'http://localhost:5000/average'
    test_microservice(f"{base_url}/daily", sample_data)
    test_microservice(f"{base_url}/weekly", sample_data)
    test_microservice(f"{base_url}/monthly", sample_data)
