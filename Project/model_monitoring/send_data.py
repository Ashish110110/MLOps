import sys
import json
import uuid
import pickle
import requests
import pandas as pd

from time import sleep
from datetime import datetime

df = pd.read_csv('winequality.csv')

with open('lin_reg.bin', 'rb') as f_in:
        (dv, lr) = pickle.load(f_in)
        
numerical = ['volatile_acidity', 'free_sulfur_dioxide', 'total_sulfur_dioxide', 'alcohol']

dicts = df[numerical].to_dict(orient='records')


class DateTimeEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime):
            return o.isoformat()
        return json.JSONEncoder.default(self, o)

i = 0

with open("target.csv", 'w') as f_target:
    for row in dicts:
        i = i + 1
        row['id'] = str(uuid.uuid4())
        X_val = dv.transform(row)
        y_pred = lr.predict(X_val)
        y_pred = str(y_pred).lstrip('[').rstrip(']')
    
        if y_pred != 0.0:
            f_target.write(f"{row['id']},{y_pred}\n")
        resp = requests.post("http://127.0.0.1:9696/predict",
                             headers={"Content-Type": "application/json"},
                             data=json.dumps(row, cls=DateTimeEncoder)).json()
        print(f"quality: {resp['quality']}")
        sleep(1)
        if i == 100:
            sys.exit(0)
