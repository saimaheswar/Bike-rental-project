"""Traffic details form: stores Normal/Abnormal traffic for the 8 directions around a station.

Run directly: python scripts/traffic_main.py
"""
import sqlite3
import sys

from PyQt5 import QtWidgets

import db
from traffic_ui import Ui_MainWindow


class TrafficWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None, db_path=db.DB_PATH):
        super().__init__(parent)
        self.db_path = db_path
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        # Inputs in db.TRAFFIC_COLUMNS order: N, NE, E, SE, S, SW, W, NW.
        self.direction_inputs = (
            self.ui.lineEdit_14,
            self.ui.lineEdit_4,
            self.ui.lineEdit_5,
            self.ui.lineEdit_6,
            self.ui.lineEdit_7,
            self.ui.lineEdit_8,
            self.ui.lineEdit_9,
            self.ui.lineEdit_10,
        )
        self.ui.pushButton.clicked.connect(self.store_traffic_details)

    def store_traffic_details(self):
        values = [line_edit.text() for line_edit in self.direction_inputs]
        try:
            row = db.insert_traffic(values, self.db_path)
        except ValueError as exc:
            QtWidgets.QMessageBox.warning(self, "Invalid traffic details", f"Nothing was saved.\n\n{exc}")
            return
        except sqlite3.Error as exc:
            QtWidgets.QMessageBox.critical(self, "Database error", f"Could not save traffic details:\n{exc}")
            return
        summary = "\n".join(f"{db.TRAFFIC_DIRECTIONS[column]}: {marker}" for column, marker in zip(db.TRAFFIC_COLUMNS, row))
        QtWidgets.QMessageBox.information(self, "Traffic details saved", f"Saved to the database:\n\n{summary}")


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = TrafficWindow()
    window.show()
    sys.exit(app.exec_())
