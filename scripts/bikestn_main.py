"""Bike station details form: stores a station's ID, name, location and contact number.

Run directly: python scripts/bikestn_main.py
"""
import sqlite3
import sys

from PyQt5 import QtWidgets

import db
from bikestn_ui import Ui_MainWindow


class BikeStationWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None, db_path=db.DB_PATH):
        super().__init__(parent)
        self.db_path = db_path
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.field_inputs = {
            "id": self.ui.lineEdit_3,
            "code": self.ui.lineEdit_4,
            "byear": self.ui.lineEdit_7,
            "city": self.ui.lineEdit_5,
            "state": self.ui.lineEdit_6,
            "country": self.ui.lineEdit,
            "ccmobile": self.ui.lineEdit_2,
        }
        self.ui.pushButton.clicked.connect(self.store_station_details)

    def store_station_details(self):
        fields = {column: line_edit.text() for column, line_edit in self.field_inputs.items()}
        try:
            row = db.insert_station(fields, self.db_path)
        except ValueError as exc:
            QtWidgets.QMessageBox.warning(self, "Invalid bike station details", f"Nothing was saved.\n\n{exc}")
            return
        except sqlite3.Error as exc:
            QtWidgets.QMessageBox.critical(self, "Database error", f"Could not save bike station details:\n{exc}")
            return
        QtWidgets.QMessageBox.information(
            self, "Bike station saved", f"Station {row[0]} ({row[1]}, {row[3]}) saved to the database."
        )


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = BikeStationWindow()
    window.show()
    sys.exit(app.exec_())
