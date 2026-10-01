"""Window plotting the sigmoid activation used by the neuron in model.py.

Run directly: python scripts/sigmoid_plot.py
"""
import sys

import numpy as np
from PyQt5 import QtWidgets
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure

from model import sigmoid


class SigmoidWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Sigmoid Function")
        figure = Figure(figsize=(6, 4), tight_layout=True)
        axes = figure.add_subplot()
        x = np.linspace(-10, 10, 100)
        axes.plot(x, sigmoid(x), c="r")
        axes.set_xlabel("x")
        axes.set_ylabel("sigmoid(x) = 1 / (1 + e^-x)")
        axes.grid(True)
        self.setCentralWidget(FigureCanvasQTAgg(figure))


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = SigmoidWindow()
    window.show()
    sys.exit(app.exec_())
