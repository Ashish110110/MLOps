import argparse
import os
import pickle
import mlflow

from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error

mlflow.set_tracking_uri("sqlite:///mlflow_one.db")
mlflow.set_experiment("week-two_homework")


def load_pickle(filename: str):
    with open(filename, "rb") as f_in:
        return pickle.load(f_in)


def run(data_path):
    
    mlflow.sklearn.autolog()
    
    with mlflow.start_run():       

        X_train, y_train = load_pickle(os.path.join(data_path, "train.pkl"))
        X_valid, y_valid = load_pickle(os.path.join(data_path, "valid.pkl"))

        rf = RandomForestRegressor(max_depth=10, random_state=0)
        rf.fit(X_train, y_train)
        y_pred = rf.predict(X_valid)

        rmse = mean_squared_error(y_valid, y_pred, squared=False)
        mlflow.log_metric("rmse", rmse)
        


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--data_path",
        default="./output",
        help="the location where the processed NYC taxi trip data was saved."
    )
    args = parser.parse_args()

    run(args.data_path)
