#!/usr/bin/env python
# coding: utf-8

import os
from datetime import datetime

import pandas as pd

year = 2021
month = 1


def dt(hour, minute, second=0):
    return datetime(2021, 1, 1, hour, minute, second)


options = {"client_kwargs": {"endpoint_url": "http://localhost:4566"}}
input_file = f"s3://nyc-duration/in/{year:04d}-{month:02d}.parquet"

data = [
    (None, None, dt(1, 2), dt(1, 10)),
    (1, 1, dt(1, 2), dt(1, 10)),
    (1, 1, dt(1, 2, 0), dt(1, 2, 50)),
    (1, 1, dt(1, 2, 0), dt(2, 2, 1)),
]

columns = ["PUlocationID", "DOlocationID", "pickup_datetime", "dropOff_datetime"]
df_input = pd.DataFrame(data, columns=columns)

df_input.to_parquet(
    input_file,
    engine="pyarrow",
    compression=None,
    index=False,
    storage_options=options,
)

os.system(f"cd .. && pipenv run python batch.py {year:04d} {month:02d}")

df = pd.read_parquet(
    f"s3://nyc-duration/out/{year:04d}-{month:02d}.parquet", storage_options=options
)
print(df)

total_duration = (df["predicted_duration"]).sum()
print(f"Total Duration : {total_duration}")
