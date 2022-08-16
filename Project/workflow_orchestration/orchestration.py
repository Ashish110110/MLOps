import pandas as pd
import pickle
import requests as req
import os

from sklearn.feature_extraction import DictVectorizer
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from datetime import date
from datetime import datetime
from datetime import timedelta
from dateutil.relativedelta import relativedelta

from prefect import flow, task, get_run_logger
from prefect.task_runners import SequentialTaskRunner
from prefect.filesystems import S3

data_dir = "./data"

@task
def read_data(filename: str):
    df = pd.read_csv(filename)
    return df

@task
def train_model(df, numerical):
    
    logger = get_run_logger()
    train_dicts = df[numerical].to_dict(orient='records')
    dv = DictVectorizer()
    X_train = dv.fit_transform(train_dicts) 
    y_train = df.quality.values

    logger.info(f"The shape of X_train is {X_train.shape}")
    logger.info(f"The DictVectorizer has {len(dv.feature_names_)} features")

    lr = LinearRegression()
    lr.fit(X_train, y_train)
    y_pred = lr.predict(X_train)
    mse = mean_squared_error(y_train, y_pred, squared=False)
    logger.info(f"The MSE of training is: {mse}")
    return lr, dv

@task
def run_model(df, numerical, dv, lr):
    logger = get_run_logger()
    val_dicts = df[numerical].to_dict(orient='records')
    X_val = dv.transform(val_dicts) 
    y_pred = lr.predict(X_val)
    y_val = df.quality.values

    mse = mean_squared_error(y_val, y_pred, squared=False)
    logger.info(f"The MSE of validation is: {mse}")
    return
        
@flow(name="main", task_runner=SequentialTaskRunner())
def main():

    numerical = ['total sulfur dioxide', 'free sulfur dioxide', 'alcohol', 'volatile acidity']

    df_train = read_data(os.path.join(data_dir, "red_wine_train.csv"))
    df_val = read_data(os.path.join(data_dir, "red_wine_val.csv"))

    # train the model
    lr, dv = train_model(df_train, numerical)
    run_model(df_val, numerical, dv, lr)
    
    with open('models/lin_reg.pkl', 'wb') as f_out:
        pickle.dump((lr), f_out)
    
    with open('models/dv.pkl', 'wb') as f_out:
        pickle.dump((dv), f_out)
    
    block = S3(bucket_path="{bucket-name}/prefect-orion", aws_access_key_id="{your aws_access_key_id}", aws_secret_access_key="{your aws_secret_access_key}")
    block.save("mlops-project-block", overwrite=True)

main()