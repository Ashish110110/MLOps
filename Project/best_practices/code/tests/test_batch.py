import math

import batch


def test_predict():

    wine_quality = {
        "total_sulfur_dioxide": 54,
        "free_sulfur_dioxide": 28,
        "alcohol": 10.4,
        "volatile_acidity": 0.46,
    }

    actual_prediction = math.floor(batch.predict(wine_quality))

    expected_prediction = 5

    assert actual_prediction == expected_prediction
