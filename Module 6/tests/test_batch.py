from datetime import datetime

import pandas as pd
from pandas.testing import assert_frame_equal

import batch


def dt(hour, minute, second=0):
    return datetime(2021, 1, 1, hour, minute, second)


def test_prepare_data():

    input_data = [
        (None, None, dt(1, 2), dt(1, 10)),
        (1, 1, dt(1, 2), dt(1, 10)),
        (1, 1, dt(1, 2, 0), dt(1, 2, 50)),
        (1, 1, dt(1, 2, 0), dt(2, 2, 1)),
    ]

    input_columns = [
        'PUlocationID',
        'DOlocationID',
        'pickup_datetime',
        'dropOff_datetime',
    ]
    input_df = pd.DataFrame(input_data, columns=input_columns)

    categorical = ["PUlocationID", "DOlocationID"]

    actual_df = batch.prepare_data(input_df, categorical)

    expected_data = [
        ("-1", "-1", dt(1, 2), dt(1, 10), 8.0),
        ("1", "1", dt(1, 2), dt(1, 10), 8.0),
    ]

    expected_columns = [
        "PUlocationID",
        "DOlocationID",
        "pickup_datetime",
        "dropOff_datetime",
        "duration",
    ]

    expected_df = pd.DataFrame(expected_data, columns=expected_columns)

    assert_frame_equal(actual_df, expected_df, check_dtype=False)
