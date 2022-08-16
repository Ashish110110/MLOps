import requests

wine_quality = {
    "total sulfur dioxide": 54,
    "free sulfur dioxide": 28,
    "alcohol": 10.4,
    "volatile acidity": 0.46
}

url = 'http://localhost:9696/predict'
response = requests.post(url, json=wine_quality)
print(response.json())