import pickle

from flask import Flask, request, jsonify

with open('lin_reg.bin', 'rb') as f_in:
    (dv, model) = pickle.load(f_in)


def prepare_features(wine_quality):
    features = {}
    (features['total_sulfur_dioxide'], features['free_sulfur_dioxide'], features['alcohol'], features['volatile_acidity']) = (wine_quality['total_sulfur_dioxide'], wine_quality['free_sulfur_dioxide'], wine_quality['alcohol'], wine_quality['volatile_acidity'])
    return features


def predict(features):
    X = dv.transform(features)
    preds = model.predict(X)
    return float(preds[0])


app = Flask('quality-prediction')


@app.route('/predict', methods=['POST'])
def predict_endpoint():
    wine_quality = request.get_json()

    features = prepare_features(wine_quality)
    pred = predict(features)

    result = {
        'quality': pred
    }

    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=9696)