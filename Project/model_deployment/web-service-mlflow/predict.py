import os

import mlflow
from flask import Flask, request, jsonify

RUN_ID = os.getenv('RUN_ID')
MLFLOW_TRACKING_URI = 'http://127.0.0.1:5000'

logged_model = f's3://{enter-the-name-of-your-S3-bucket-here}/1/{RUN_ID}/artifacts/model'
model = mlflow.pyfunc.load_model(logged_model)

def prepare_features(wine_quality):
    features = {}
    (features['total sulfur dioxide'], features['free sulfur dioxide'], features['alcohol'], features['volatile acidity']) = (wine_quality['total sulfur dioxide'], wine_quality['free sulfur dioxide'], wine_quality['alcohol'], wine_quality['volatile acidity'])
    return features


def predict(features):
    preds = model.predict(features)
    return float(preds[0])


app = Flask('wine-quality-prediction')


@app.route('/predict', methods=['POST'])
def predict_endpoint():
    wine_quality = request.get_json()

    features = prepare_features(wine_quality)
    pred = predict(features)

    result = {
        'quality': pred,
        'model_version': RUN_ID
    }

    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=9696)