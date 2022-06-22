#!/usr/bin/env python
# coding: utf-8



# get_ipython().system('pip freeze | grep scikit-learn')

import pickle
import mlflow
import os
import pandas as pd
import sys
import boto3

from sklearn.feature_extraction import DictVectorizer
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error

os.environ["AWS_PROFILE"] = "ashish013"


with open('model.bin', 'rb') as f_in:
    dv, lr = pickle.load(f_in)


categorical = ['PUlocationID', 'DOlocationID']

def read_data(filename):
    df = pd.read_parquet(filename)
    
    # df.to_parquet('df.parquet.gzip',
    #               compression='gzip',
    #               engine='pyarrow',
    #               index=False       
    # )
    
    df['duration'] = df.dropOff_datetime - df.pickup_datetime
    df['duration'] = df.duration.dt.total_seconds() / 60

    df = df[(df.duration >= 1) & (df.duration <= 60)].copy()

    df[categorical] = df[categorical].fillna(-1).astype('int').astype('str')
    
    return df

# df = read_data('https://nyc-tlc.s3.amazonaws.com/trip+data/fhv_tripdata_2021-02.parquet')


# dicts = df[categorical].to_dict(orient='records')
# X_val = dv.transform(dicts)
# y_pred = lr.predict(X_val)

# year = 2021
# month = 2
# df['ride_id'] = f'{year:04d}/{month:02d}_' + df.index.astype('str')

# df_result = pd.DataFrame()
# df_result['ride_id'] = df['ride_id']
# df_result['pickup_datetime'] = df['pickup_datetime']
# df_result['PUlocationID'] = df['PUlocationID']
# df_result['DOlocationID'] = df['DOlocationID']
# df_result['actual_duration'] = df['duration']
# df_result['predicted_duration'] = y_pred
# df_result['diff'] = df_result['actual_duration'] - df_result['predicted_duration']

# print("Mean Predicted Duration : ", df_result['predicted_duration'].mean())

#output_file = f'output/{year:04d}-{month:02d}.parquet'

# df_result.to_parquet(
#     output_file,
#     engine='pyarrow',
#     compression=None,
#     index=False
# )


def apply_model(input_file, output_file, year, month):
    print(f'reading the data from {input_file}...')
    df = read_data(input_file)
    dicts = df[categorical].to_dict(orient='records')
    X_val = dv.transform(dicts)
    df['ride_id'] = f'{year:04d}/{month:02d}_' + df.index.astype('str')
    
    print(f'applying the model...')
    y_pred = lr.predict(X_val)
    
    print(f'saving the result to {output_file}...')
    df_result = pd.DataFrame()
    df_result['ride_id'] = df['ride_id']
    df_result['pickup_datetime'] = df['pickup_datetime']
    df_result['PUlocationID'] = df['PUlocationID']
    df_result['DOlocationID'] = df['DOlocationID']
    df_result['actual_duration'] = df['duration']
    df_result['predicted_duration'] = y_pred
    df_result['diff'] = df_result['actual_duration'] - df_result['predicted_duration']
    
    df_result.to_parquet(
        output_file,
        engine='pyarrow',
        compression=None,
        index=False
    )
    
    print(f'Successfully saved the result!')
    print("Mean Predicted Duration : ", df_result['predicted_duration'].mean())
    
    print(f'uploading output parquet file to Amazon S3 Bucket...')
    s3 = boto3.resource('s3')
    BUCKET = "mlflow-ssh-new"
    
    s3.Bucket(BUCKET).upload_file(output_file, f'mlops-week-4/{year:04d}-{month:02d}.parquet')
    
    print(f'uploaded output parquet file to Amazon S3 Bucket successfully!')

def run():
    year = int(sys.argv[1]) # 2021
    month = int(sys.argv[2]) # 2
    
    input_file = f'https://s3.amazonaws.com/nyc-tlc/trip+data/fhv_tripdata_{year:04d}-{month:02d}.parquet'  # https://nyc-tlc.s3.amazonaws.com/trip+data/fhv_tripdata_2021-03.parquet
    output_file = f'output/{year:04d}-{month:02d}.parquet'
    
    apply_model(input_file=input_file,  
                output_file=output_file,
                year=year,
                month=month
    )
    
if __name__ == '__main__':
    run()
