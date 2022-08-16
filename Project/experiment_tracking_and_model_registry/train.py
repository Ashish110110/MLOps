import os
import pickle
import mlflow
import argparse

from sklearn.metrics import mean_squared_error
from sklearn.ensemble import RandomForestRegressor

os.environ["AWS_PROFILE"] = "default"

mlflow.set_tracking_uri("http://127.0.0.1:5000")
mlflow.set_experiment("red-wine-quality-prediction")


def load_pickle(filename: str):
    with open(filename, "rb") as f_in:
        return pickle.load(f_in)


def run(data_path):
    
    mlflow.sklearn.autolog()
    
    with mlflow.start_run():       

        X_train, y_train = load_pickle(os.path.join(data_path, "train.pkl"))
        X_valid, y_valid = load_pickle(os.path.join(data_path, "valid.pkl"))

        rf = RandomForestRegressor(max_depth=10, n_estimators=100, min_samples_leaf=10, random_state=0)
        rf.fit(X_train, y_train)
        y_pred = rf.predict(X_valid)

        rmse = mean_squared_error(y_valid, y_pred, squared=False)
        mlflow.log_metric("rmse", rmse)


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--data_path",
        default="./output",
        help="the location where the processed red wine quality data was saved."
    )
    args = parser.parse_args()

    run(args.data_path)