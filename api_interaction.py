import requests

# URL of the API endpoint
url = "https://api.example.com/data"

# Optional: Parameters for the API request
params = {'key1': 'value1', 'key2': 'value2'}

# Sending a GET request to the API and storing the response
response = requests.get(url, params=params)

# Check if the request was successful
if response.status_code == 200:
    # Process the JSON data returned
    data = response.json()
    print("Data retrieved:", data)
else:
    print("Failed to retrieve data")
