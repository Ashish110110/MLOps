import pandas as pd
import pickle
# import mlflow

from sklearn.feature_extraction import DictVectorizer
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from datetime import date
from datetime import datetime
from datetime import timedelta


from prefect import flow, task, get_run_logger
from prefect.task_runners import SequentialTaskRunner
from prefect.deployments import DeploymentSpec
from prefect.orion.schemas.schedules import CronSchedule
from prefect.orion.schemas.schedules import IntervalSchedule
from prefect.flow_runners import SubprocessFlowRunner


@task
def read_data(path):
    df = pd.read_parquet(path)
    return df

@task
def prepare_features(df, categorical, train=True):
    logger = get_run_logger()
    df['duration'] = df.dropOff_datetime - df.pickup_datetime
    df['duration'] = df.duration.dt.total_seconds() / 60
    df = df[(df.duration >= 1) & (df.duration <= 60)].copy()

    mean_duration = df.duration.mean()
    if train:
        logger.info(f"The mean duration of training is {mean_duration}")
    else:
        logger.info(f"The mean duration of validation is {mean_duration}")
    
    df[categorical] = df[categorical].fillna(-1).astype('int').astype('str')
    return df

@task
def train_model(df, categorical):
    
    logger = get_run_logger()
    train_dicts = df[categorical].to_dict(orient='records')
    dv = DictVectorizer()
    X_train = dv.fit_transform(train_dicts) 
    y_train = df.duration.values

    logger.info(f"The shape of X_train is {X_train.shape}")
    logger.info(f"The DictVectorizer has {len(dv.feature_names_)} features")

    lr = LinearRegression()
    lr.fit(X_train, y_train)
    y_pred = lr.predict(X_train)
    mse = mean_squared_error(y_train, y_pred, squared=False)
    logger.info(f"The MSE of training is: {mse}")
    return lr, dv

@task
def run_model(df, categorical, dv, lr):
    logger = get_run_logger()
    val_dicts = df[categorical].to_dict(orient='records')
    X_val = dv.transform(val_dicts) 
    y_pred = lr.predict(X_val)
    y_val = df.duration.values

    mse = mean_squared_error(y_val, y_pred, squared=False)
    logger.info(f"The MSE of validation is: {mse}")
    return

@task
def get_paths(user_date):
    if user_date == None:
        today = date.today()
        train_data_month = str(today.month - 2).zfill(2)
        val_data_month = str(today.month - 1).zfill(2)
        train_path = "data/fhv_tripdata_{}-{}.parquet".format(today.year, train_data_month)
        val_path = "data/fhv_tripdata_{}-{}.parquet".format(today.year, val_data_month)
        
        
#         print(today)
#         print(train_data_month)
#         print(val_data_month)
#         print(train_path)
#         print(val_path)
        
    
    else:
        user_date = datetime.strptime(user_date, '%Y-%m-%d')
        train_data_month = str(user_date.month - 2).zfill(2)
        val_data_month = str(user_date.month - 1).zfill(2)
        train_path = "data/fhv_tripdata_{}-{}.parquet".format(user_date.year, train_data_month)
        val_path = "data/fhv_tripdata_{}-{}.parquet".format(user_date.year, val_data_month)
#         print(user_date)
#         print(train_path)
#         print(val_path)
        
    return train_path, val_path

@flow(task_runner=SequentialTaskRunner())
def main(user_date=None):
    
    train_path, val_path = get_paths(user_date).result()
    categorical = ['PUlocationID', 'DOlocationID']

    df_train = read_data(train_path)
    df_train_processed = prepare_features(df_train, categorical)

    df_val = read_data(val_path)
    df_val_processed = prepare_features(df_val, categorical)

    # train the model
    lr, dv = train_model(df_train_processed, categorical).result()
    run_model(df_val_processed, categorical, dv, lr)
    
    with open('models/model-{}.pkl'.format(user_date), 'wb') as f_out:
        pickle.dump((lr), f_out)
    
    with open('models/dv-{}.pkl'.format(user_date), 'wb') as f_out_one:
        pickle.dump((dv), f_out_one)

# main(user_date="2021-08-15")

DeploymentSpec(
    flow=main,
    name="model_training",
    schedule=CronSchedule(cron="0 9 15 * *"),
    flow_runner=SubprocessFlowRunner(),
    tags=["ml"],
)

