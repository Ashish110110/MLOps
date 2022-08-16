import requests

url = 'http://127.0.0.1:9696/predict'

wine_quality = {
    "volatile_acidity": 0.46,
    "free_sulfur_dioxide": 28,
    "total_sulfur_dioxide": 54,
    "alcohol": 10.4,
    
}


response = requests.post(url, json=wine_quality).json()
print(response)
