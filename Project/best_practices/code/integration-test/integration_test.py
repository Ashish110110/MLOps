#!/usr/bin/env python
# coding: utf-8

import os

import pandas as pd

options = {"client_kwargs": {"endpoint_url": "http://localhost:4566"}}
input_file = f"s3://red-wine-quality/in/red_wine_train.csv"

data = [
    (0.7, 11.0, 34.0, 9.4),
    (0.6, 15.0, 59.0, 9.4),
    (0.65, 15.0, 21.0, 10.0),
]

columns = ["volatile_acidity", "free_sulfur_dioxide", "total_sulfur_dioxide", "alcohol"]
df_input = pd.DataFrame(data, columns=columns)

df_input.to_csv(
    input_file,
    compression=None,
    index=False,
    storage_options=options,
)

os.system(f"cd .. && pipenv run python batch.py")

df = pd.read_csv(f"s3://red-wine-quality/out/predictions.csv", storage_options=options)
print("printing predictions.csv....")
print(df)
