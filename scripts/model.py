"""Single-neuron neural network, written from scratch in numpy, that predicts
whether a bike station is important from the traffic in the 8 directions
around it (1 = abnormal traffic, 0 = normal).

Run directly to train on data/bikeset.csv and print the weights, held-out
metrics and sample predictions:  python scripts/model.py
"""
import os

import numpy as np
import pandas as pd

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(REPO_ROOT, "data", "bikeset.csv")

DIRECTIONS = ("N", "NE", "E", "SE", "S", "SW", "W", "NW")
FEATURE_COLUMNS = [f"{direction}_Traffic" for direction in DIRECTIONS]
LABEL_COLUMN = "Importance?"
LABELS = {"Important": 1.0, "Normal": 0.0}

EPOCHS = 2000
LEARNING_RATE = 10.0
TEST_FRACTION = 0.2
SEED = 42
THRESHOLD = 0.5

SAMPLE_PATTERNS = (
    (1, 1, 1, 1, 1, 1, 1, 1),
    (1, 0, 0, 1, 0, 0, 0, 1),
    (1, 0, 1, 0, 1, 1, 1, 1),
)


def sigmoid(x):
    return 1.0 / (1.0 + np.exp(-x))


def load_data(path=DATA_PATH):
    """Read the dataset and return (features, labels).

    features is an (n, 8) 0/1 matrix in DIRECTIONS order (1 = abnormal traffic);
    labels is an (n, 1) 0/1 column (1 = important station).
    """
    df = pd.read_csv(path)
    missing = [column for column in FEATURE_COLUMNS + [LABEL_COLUMN] if column not in df.columns]
    if missing:
        raise ValueError(f"{path} is missing column(s): {', '.join(missing)}")

    # Values look like "North_Abnormal", "NE_Normal", "South_normal": the suffix carries the state.
    states = df[FEATURE_COLUMNS].apply(lambda column: column.str.rsplit("_", n=1).str[-1].str.lower())
    unknown = ~states.isin(["normal", "abnormal"])
    if unknown.any().any():
        bad_columns = ", ".join(states.columns[unknown.any()])
        raise ValueError(f"{path} has traffic values that are neither Normal nor Abnormal in: {bad_columns}")
    labels = df[LABEL_COLUMN].map(LABELS)
    if labels.isna().any():
        raise ValueError(f"{path} has {LABEL_COLUMN} values other than {', '.join(LABELS)}")

    features = (states == "abnormal").to_numpy(dtype=float)
    return features, labels.to_numpy(dtype=float).reshape(-1, 1)


def split_data(features, labels, test_fraction=TEST_FRACTION, seed=SEED):
    """Shuffle rows with a fixed seed and hold out test_fraction of them.

    Returns (train_features, train_labels, test_features, test_labels).
    """
    order = np.random.default_rng(seed).permutation(len(features))
    test_size = int(round(len(features) * test_fraction))
    test, train_rows = order[:test_size], order[test_size:]
    return features[train_rows], labels[train_rows], features[test], labels[test]


def train(features, labels, epochs=EPOCHS, learning_rate=LEARNING_RATE, seed=SEED):
    """Fit the neuron with full-batch gradient descent on mean squared error.

    Returns (weights, bias): an (8, 1) array and a float.
    """
    rng = np.random.default_rng(seed)
    weights = rng.random((features.shape[1], 1))
    bias = rng.random()
    for _ in range(epochs):
        # Feedforward: weighted sum of the inputs, squashed by the sigmoid.
        predictions = sigmoid(features @ weights + bias)

        # Backpropagation (chain rule): dCost/dPred = error, and dPred/dSum = s * (1 - s)
        # where s is the sigmoid *output*. Gradients are averaged over the rows.
        error = predictions - labels
        delta = error * predictions * (1.0 - predictions)
        weights -= learning_rate * features.T @ delta / len(features)
        bias -= learning_rate * delta.mean()
    return weights, float(bias)


def predict(weights, bias, features):
    """Probability that each traffic pattern (a row of 8 0/1 flags) is an important station."""
    return sigmoid(np.atleast_2d(features) @ weights + bias).ravel()


def evaluate(weights, bias, features, labels, threshold=THRESHOLD):
    """Accuracy, precision and recall of the predictions thresholded at `threshold`."""
    predicted = predict(weights, bias, features) >= threshold
    actual = labels.ravel() == 1
    true_positives = np.sum(predicted & actual)
    false_positives = np.sum(predicted & ~actual)
    false_negatives = np.sum(~predicted & actual)
    predicted_positives = true_positives + false_positives
    actual_positives = true_positives + false_negatives
    return {
        "accuracy": float(np.mean(predicted == actual)),
        "precision": float(true_positives / predicted_positives) if predicted_positives else 0.0,
        "recall": float(true_positives / actual_positives) if actual_positives else 0.0,
    }


def train_and_evaluate(path=DATA_PATH):
    """Train on a seeded 80/20 split of the dataset; returns (weights, bias, test metrics)."""
    train_features, train_labels, test_features, test_labels = split_data(*load_data(path))
    weights, bias = train(train_features, train_labels)
    return weights, bias, evaluate(weights, bias, test_features, test_labels)


def format_weights(weights, bias):
    lines = [f"{direction:>2}: {weight:+.4f}" for direction, weight in zip(DIRECTIONS, weights.ravel())]
    return "Final adjusted weights:\n" + "\n".join(lines) + f"\nbias: {bias:+.4f}"


def format_metrics(metrics):
    lines = [f"{name}: {value:.4f}" for name, value in metrics.items()]
    return f"Held-out test set ({TEST_FRACTION:.0%} of rows, seed {SEED}):\n" + "\n".join(lines)


def format_predictions(weights, bias, patterns=SAMPLE_PATTERNS):
    probabilities = predict(weights, bias, np.array(patterns, dtype=float))
    lines = [
        f"{','.join(map(str, pattern))} -> {probability:.4f} "
        f"({'Important' if probability >= THRESHOLD else 'Normal'})"
        for pattern, probability in zip(patterns, probabilities)
    ]
    return f"Station importance for traffic patterns ({','.join(DIRECTIONS)}):\n" + "\n".join(lines)


if __name__ == "__main__":
    weights, bias, metrics = train_and_evaluate()
    print(format_weights(weights, bias), format_metrics(metrics), format_predictions(weights, bias), sep="\n\n")
