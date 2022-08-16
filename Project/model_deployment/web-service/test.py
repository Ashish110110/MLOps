import requests

wine_quality = {
    "total_sulfur_dioxide": 54,
    "free_sulfur_dioxide": 28,
    "alcohol": 10.4,
    "volatile_acidity": 0.46
}

url = 'http://localhost:9696/predict'
response = requests.post(url, json=wine_quality)
print(response.json())