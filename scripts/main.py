"""Main menu of the Station Importance Evaluation app.

Run from anywhere: python scripts/main.py
"""
import sqlite3
import sys

from PyQt5 import QtWidgets

import model
from bikerental_ui import Ui_MainWindow
from bikestn_main import BikeStationWindow
from export_csv import CSV_PATH, export_traffic_csv
from sigmoid_plot import SigmoidWindow
from traffic_main import TrafficWindow


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self._windows = {}
        self._trained_model = None

        self.ui.pushButton.clicked.connect(self.show_traffic_details)
        self.ui.pushButton_2.clicked.connect(self.create_csv)
        self.ui.pushButton_3.clicked.connect(self.show_bike_station_details)
        self.ui.pushButton_4.clicked.connect(self.plot_sigmoid)
        self.ui.pushButton_5.clicked.connect(self.show_weights)
        self.ui.pushButton_6.clicked.connect(self.show_predictions)

    def show_traffic_details(self):
        self._show_window(TrafficWindow)

    def show_bike_station_details(self):
        self._show_window(BikeStationWindow)

    def plot_sigmoid(self):
        self._show_window(SigmoidWindow)

    def create_csv(self):
        try:
            count = export_traffic_csv()
        except (sqlite3.Error, OSError) as exc:
            QtWidgets.QMessageBox.critical(self, "Create CSV", f"Could not export traffic details:\n{exc}")
            return
        QtWidgets.QMessageBox.information(self, "Create CSV", f"Exported {count} traffic row(s) to:\n{CSV_PATH}")

    def show_weights(self):
        trained = self._train_once()
        if trained:
            weights, bias, _ = trained
            QtWidgets.QMessageBox.information(self, "Weights", model.format_weights(weights, bias))

    def show_predictions(self):
        trained = self._train_once()
        if trained:
            weights, bias, metrics = trained
            report = model.format_metrics(metrics) + "\n\n" + model.format_predictions(weights, bias)
            QtWidgets.QMessageBox.information(self, "Prediction", report)

    def _show_window(self, window_class):
        """Show the single instance of window_class, creating it on first use."""
        window = self._windows.get(window_class)
        if window is None:
            window = self._windows[window_class] = window_class(parent=self)
        window.show()
        window.raise_()
        window.activateWindow()

    def _train_once(self):
        """Train the model on first use and cache it; returns None if the dataset cannot be loaded."""
        if self._trained_model is None:
            try:
                self._trained_model = model.train_and_evaluate()
            except (OSError, ValueError) as exc:
                QtWidgets.QMessageBox.critical(self, "Model", f"Could not train the model:\n{exc}")
        return self._trained_model


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
