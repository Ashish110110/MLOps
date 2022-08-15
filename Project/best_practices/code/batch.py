import os
import pickle

import pandas as pd


def get_input_path():
    default_input_pattern = 'https://raw.githubusercontent.com/Ashish110110/MLOps/main/Project/dataset/red_wine_train.csv'
    input_pattern = os.getenv('INPUT_FILE_PATTERN', default_input_pattern)
    return input_pattern


def get_output_path():
    default_output_pattern = 's3://red-wine-quality/predictions.csv'
    output_pattern = os.getenv('OUTPUT_FILE_PATTERN', default_output_pattern)
    return output_pattern


def prepare_features(wine_quality):
    features = {}
    (features['total_sulfur_dioxide'], features['free_sulfur_dioxide'], features['alcohol'], features['volatile_acidity']) = (wine_quality['total_sulfur_dioxide'], wine_quality['free_sulfur_dioxide'], wine_quality['alcohol'], wine_quality['volatile_acidity'])
    return features


def prepare_data(df):
    df = df.rename(columns = {'volatile acidity' : 'volatile_acidity', 'free sulfur dioxide' : 'free_sulfur_dioxide', 'total sulfur dioxide' : 'total_sulfur_dioxide'})
    return df


def predict(features):

    with open('lin_reg.bin', 'rb') as f_in:
        (dv, model) = pickle.load(f_in)

    X = dv.transform(features)
    preds = model.predict(X)
    return float(preds[0])


def read_data(filename):
    S3_ENDPOINT_URL = os.getenv("S3_ENDPOINT")

    options = {'client_kwargs': {'endpoint_url': S3_ENDPOINT_URL}}

    return pd.read_csv(filename, storage_options=options)


def save_data(df, filename):
    S3_ENDPOINT_URL = os.getenv("S3_ENDPOINT")

    options = {'client_kwargs': {'endpoint_url': S3_ENDPOINT_URL}}

    df.to_csv(
        filename,
        compression=None,
        index=False,
        storage_options=options,
    )


def main():

    input_file = get_input_path()
    output_file = get_output_path()

    with open('lin_reg.bin', 'rb') as f_in:
        (dv, lr) = pickle.load(f_in)

    numerical = ['volatile_acidity', 'free_sulfur_dioxide', 'total_sulfur_dioxide', 'alcohol']

    df = read_data(input_file)
    df = prepare_data(df)

    dicts = df[numerical].to_dict(orient='records')
    X_val = dv.transform(dicts)
    y_pred = lr.predict(X_val)

    df_result = pd.DataFrame()
    df_result['predicted_wine_quality'] = y_pred

    save_data(df_result, output_file)


if __name__ == '__main__':
    main()
