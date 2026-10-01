# Station Importance Evaluation in a Dynamic Bike-Rental System

A PyQt5 desktop app that records traffic around bike stations in SQLite and uses a
single-neuron neural network, written from scratch in numpy, to predict which
stations are **important**.

## The idea

A bike station is surrounded by 8 directions (N, NE, E, SE, S, SW, W, NW). For each
direction, traffic is marked **Abnormal (A)** when the difference between incoming
and outgoing bikes is more than 4 in the next half hour, and **Normal (N)** otherwise.
The pattern of abnormal directions says a lot about a station: one that is unbalanced
on many sides at once needs priority for rebalancing and capacity. The network learns
that mapping from 8 Normal/Abnormal flags to an importance score from labelled
historical data (`data/bikeset.csv`, 2,588 rows).

## File map

```
Bike-rental-project/
├── brental1                 SQLite database (tables: traffic, bikestn)
├── data/
│   ├── bikeset.csv          labelled training data (8 traffic columns + "Importance?")
│   └── traffic1.csv         output of "Create CSV" (traffic table export)
├── ui/                      Qt Designer sources (*.ui)
└── scripts/
    ├── main.py              main menu window; opens every other feature
    ├── traffic_main.py      traffic details form -> traffic table
    ├── bikestn_main.py      bike station details form -> bikestn table
    ├── db.py                schema, input validation, parameterized inserts
    ├── export_csv.py        traffic table -> data/traffic1.csv
    ├── model.py             the neural network: load_data, train, evaluate, predict
    ├── sigmoid_plot.py      plot of the activation function
    ├── validate.py          end-to-end checks (model + database)
    └── *_ui.py              generated from ui/*.ui by pyuic5 (do not edit)
```

## Setup

Requires Python 3.12+ (tested on 3.14).

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Running

Every script resolves its paths from its own location, so they work from any directory.

```bash
python scripts/main.py        # the full app
python scripts/model.py       # train and print weights, test metrics, sample predictions
python scripts/export_csv.py  # export the traffic table to data/traffic1.csv
python scripts/validate.py    # run the checks; exit code 0 = all passed
```

The main menu buttons:

| Button               | What it does                                                               |
|----------------------|----------------------------------------------------------------------------|
| Bike Station Details | Form for a station's ID, name, city, state, country, year, contact number |
| Traffic Details      | Form for the 8 directions; enter `N` or `A` in each box                    |
| Create CSV           | Exports the `traffic` table to `data/traffic1.csv`                         |
| Plot the Sigmoid     | Plots the network's activation function                                    |
| Weights              | Trains the network (once per session) and shows the learned weights        |
| Prediction           | Shows held-out accuracy/precision/recall and sample predictions            |

Both forms validate input before anything is written: traffic boxes accept only
`N`/`A` (or `Normal`/`Abnormal`, any case), and station fields are checked for
required values, length limits, a 4-digit build year that is not in the future,
a phone number of 7-14 digits, and a station ID that is not already taken.
Nothing is saved if any field is invalid. All inserts use parameterized SQL.

## How the neural network works

The model is one neuron: it takes the 8 traffic flags (1 = abnormal), computes a
weighted sum plus a bias, and passes it through a sigmoid to get a probability that
the station is important (>= 0.5 means important). Training is full-batch gradient
descent on mean squared error: each epoch runs the forward pass, computes the error
against the labels, backpropagates it through the sigmoid with the chain rule
(`error * s * (1 - s)`), and nudges the weights and bias against the averaged
gradient. Data is split 80/20 with a fixed seed; the model trains on 80% and is
scored on the held-out 20%.

### Results

On the 518 held-out rows: **accuracy 1.000, precision 1.000, recall 1.000**.

That perfect score is expected rather than suspicious. In this dataset a station is
labelled Important exactly when 5 or more of its 8 directions are abnormal. That is
a linear threshold, which a single neuron can represent exactly. The trained
weights show it: every direction gets roughly the same weight (about 4.7) and the
bias (about -21) puts the decision boundary at 4.5 abnormal directions.

## Database

`brental1` holds two tables. They are created automatically if the file is missing.

- `traffic(n, ne, e, se, s, sw, w, nw)`: one row per observation, each value `N` or `A`
- `bikestn(id, code, byear, city, state, country, ccmobile)`: `code` is the station name

## 60-second demo

1. **(0-10s)** `python scripts/main.py`. "Each button is one stage of the pipeline: collect data, export it, train, predict."
2. **(10-25s)** Click **Traffic Details**, type `A` into five of the boxes, then click **Store Traffic Details in Data base**. A confirmation lists what was saved. Type `X` into one box and store again to show that bad input is rejected and nothing is written.
3. **(25-32s)** Click **Create CSV** and open `data/traffic1.csv` to show the new row.
4. **(32-40s)** Click **Plot the Sigmoid**. "This is the neuron's activation: any weighted sum becomes a probability between 0 and 1."
5. **(40-50s)** Click **Weights**. "All 8 directions get about the same weight. The network found that it is how *many* directions are abnormal that matters, not which ones."
6. **(50-60s)** Click **Prediction**. Show the held-out metrics, then the samples: three abnormal directions gives about 0.001 (Normal), six gives about 0.999 (Important).

## Regenerating the UI code

After editing a form in Qt Designer, regenerate its Python module from the repo root:

```bash
pyuic5 ui/traffic.ui -o scripts/traffic_ui.py
```
