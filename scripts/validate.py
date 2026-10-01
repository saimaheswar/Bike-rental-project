"""End-to-end checks for the model and the database layer.

Run from anywhere: python scripts/validate.py   (exit code 0 means every check passed)
The real database is never touched; database checks use a temporary SQLite file.
"""
import csv
import os
import sys
import tempfile

import numpy as np

import db
import model
from export_csv import export_traffic_csv


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def expect_value_error(action, message):
    try:
        action()
    except ValueError:
        return
    raise AssertionError(message)


def check_model_api():
    names = ("load_data", "train", "evaluate", "predict")
    missing = [name for name in names if not callable(getattr(model, name, None))]
    require(not missing, f"model.py does not expose: {', '.join(missing)}")
    return ", ".join(names)


def check_metric_math():
    # A neuron that predicts "important" exactly when the first direction is abnormal.
    weights = np.zeros((8, 1))
    weights[0] = 20.0
    bias = -10.0
    features = np.zeros((5, 8))
    features[:3, 0] = 1  # predictions: 1, 1, 1, 0, 0
    labels = np.array([[1], [0], [0], [1], [0]])  # TP=1, FP=2, FN=1, TN=1
    metrics = model.evaluate(weights, bias, features, labels)
    expected = {"accuracy": 2 / 5, "precision": 1 / 3, "recall": 1 / 2}
    for name, value in expected.items():
        require(np.isclose(metrics[name], value), f"{name} is {metrics[name]}, expected {value}")
    return "known confusion matrix gives accuracy 0.4, precision 0.333, recall 0.5"


def check_trained_metrics():
    features, labels = model.load_data()
    require(features.shape == (len(labels), 8), f"unexpected feature shape {features.shape}")
    weights, bias, metrics = model.train_and_evaluate()
    require(set(metrics) == {"accuracy", "precision", "recall"}, f"unexpected metrics {sorted(metrics)}")
    for name, value in metrics.items():
        require(0.0 <= value <= 1.0, f"{name}={value} is outside 0-1")
    require(metrics["accuracy"] >= 0.9, f"accuracy {metrics['accuracy']:.4f} is implausibly low")
    probabilities = model.predict(weights, bias, np.array(model.SAMPLE_PATTERNS))
    require(np.all((probabilities >= 0) & (probabilities <= 1)), "predict() returned values outside 0-1")
    return ", ".join(f"{name}={value:.4f}" for name, value in metrics.items())


def check_traffic_roundtrip():
    with tempfile.TemporaryDirectory() as tmp:
        db_path = os.path.join(tmp, "validate.db")
        row = db.insert_traffic(["n", "Abnormal", " A ", "normal", "N", "A", "N", "a"], db_path)
        expected = ("N", "A", "A", "N", "N", "A", "N", "A")
        require(row == expected, f"inserted {row}, expected {expected}")
        require(db.fetch_traffic(db_path) == [expected], "row read back does not match the inserted row")

        expect_value_error(lambda: db.insert_traffic(["N"] * 7 + ["X"], db_path), "marker 'X' was accepted")
        expect_value_error(lambda: db.insert_traffic(["N"] * 7, db_path), "7 values were accepted")
        expect_value_error(lambda: db.insert_traffic(["N"] * 7 + ["N'); DROP TABLE traffic;--"], db_path),
                           "SQL-shaped input was accepted")
        require(db.fetch_traffic(db_path) == [expected], "a rejected row reached the database")

        csv_path = os.path.join(tmp, "traffic.csv")
        require(export_traffic_csv(csv_path, db_path) == 1, "CSV export did not report 1 row")
        with open(csv_path, newline="") as csv_file:
            exported = list(csv.reader(csv_file))
        require(exported == [list(db.TRAFFIC_COLUMNS), list(expected)], f"CSV export wrote {exported}")
    return "insert, read-back, rejection of bad input, CSV export"


def check_station_roundtrip():
    station = {"id": "002", "code": "Gachibowli", "byear": "2015", "city": "Hyderabad",
               "state": "Telangana", "country": "India", "ccmobile": "+919876543210"}
    with tempfile.TemporaryDirectory() as tmp:
        db_path = os.path.join(tmp, "validate.db")
        row = db.insert_station(station, db_path)
        require(db.fetch_stations(db_path) == [row], "station read back does not match the inserted row")
        expect_value_error(lambda: db.insert_station(station, db_path), "duplicate station ID was accepted")
        for column, bad_value in (("byear", "20x5"), ("byear", "2999"), ("ccmobile", "call me"), ("city", "  ")):
            expect_value_error(lambda: db.insert_station({**station, "id": "003", column: bad_value}, db_path),
                               f"{column}={bad_value!r} was accepted")
        require(len(db.fetch_stations(db_path)) == 1, "a rejected station reached the database")
    return "insert, read-back, duplicate ID and bad-field rejection"


CHECKS = (
    ("model.py exposes load_data/train/evaluate/predict", check_model_api),
    ("evaluate() computes accuracy/precision/recall correctly", check_metric_math),
    ("trained model reports sane held-out metrics", check_trained_metrics),
    ("traffic row round-trips through a temp SQLite DB", check_traffic_roundtrip),
    ("bike station row round-trips through a temp SQLite DB", check_station_roundtrip),
)


def main():
    failures = 0
    for name, check in CHECKS:
        try:
            detail = check()
        except Exception as exc:  # report every check instead of stopping at the first failure
            failures += 1
            print(f"FAIL  {name}\n      {type(exc).__name__}: {exc}")
        else:
            print(f"PASS  {name}\n      {detail}")
    print(f"\n{len(CHECKS) - failures}/{len(CHECKS)} checks passed")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
