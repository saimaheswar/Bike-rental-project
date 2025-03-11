# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'bikerental.ui'
#
# Created by: PyQt5 UI code generator 5.12.1
#
# WARNING! All changes made in this file will be lost!

import subprocess  # This allows us to run other Python files
import os  # To handle file paths
from PyQt5 import QtCore, QtGui, QtWidgets

print("🚀 Script started...")  # Debugging print

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        print("✅ Setting up the UI...")  # Debugging print

        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(514, 321)
        MainWindow.setStyleSheet("color: rgb(85, 0, 255);\n"
                                 "font: 75 12pt \"MS Shell Dlg 2\";")

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(100, 60, 321, 31))
        self.pushButton.setObjectName("pushButton")

        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(100, 110, 321, 31))
        self.pushButton_2.setObjectName("pushButton_2")

        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(100, 10, 321, 31))
        self.pushButton_3.setObjectName("pushButton_3")

        self.pushButton_4 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_4.setGeometry(QtCore.QRect(100, 160, 321, 31))
        self.pushButton_4.setObjectName("pushButton_4")

        self.pushButton_5 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_5.setGeometry(QtCore.QRect(100, 210, 321, 31))
        self.pushButton_5.setObjectName("pushButton_5")

        self.pushButton_6 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_6.setGeometry(QtCore.QRect(100, 260, 321, 31))
        self.pushButton_6.setObjectName("pushButton_6")

        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        # 🔹 Connect buttons to actual functions
        self.pushButton.clicked.connect(self.show_traffic_details)
        self.pushButton_2.clicked.connect(self.create_csv)
        self.pushButton_3.clicked.connect(self.show_bike_station_details)
        self.pushButton_4.clicked.connect(self.plot_sigmoid)
        self.pushButton_5.clicked.connect(self.show_weights)
        self.pushButton_6.clicked.connect(self.show_predictions)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Station Importance Evaluation in Dynamic Bike-Rental System"))
        self.pushButton.setText(_translate("MainWindow", "Traffic Details"))
        self.pushButton_2.setText(_translate("MainWindow", "Create CSV"))
        self.pushButton_3.setText(_translate("MainWindow", "Bike Station Details"))
        self.pushButton_4.setText(_translate("MainWindow", "Plot the Sigmoid"))
        self.pushButton_5.setText(_translate("MainWindow", "Weights"))
        self.pushButton_6.setText(_translate("MainWindow", "Prediction"))

    # 🔹 Button Functions - Execute Python Scripts with Better Handling
    def show_traffic_details(self):
        print("🚦 Opening Traffic Details...")
        try:
            traffic_script = os.path.abspath("traffic.py")  # Get the full path of traffic.py
            subprocess.run(["python3", traffic_script], check=True)
        except FileNotFoundError:
            print("❌ Error: traffic.py not found!")
        except subprocess.CalledProcessError as e:
            print(f"❌ Error running traffic.py: {e}")

    def create_csv(self):
        print("📁 Creating CSV file...")
        try:
            subprocess.run(["python3", os.path.abspath("createcsv1.py")], check=True)
        except FileNotFoundError:
            print("❌ Error: createcsv1.py not found!")

    def show_bike_station_details(self):
        print("🚲 Showing Bike Station Details...")
        try:
            subprocess.run(["python3", os.path.abspath("bikestn.py")], check=True)
        except FileNotFoundError:
            print("❌ Error: bikestn.py not found!")

    def plot_sigmoid(self):
        print("📈 Plotting Sigmoid Curve...")
        try:
            subprocess.run(["python3", os.path.abspath("sgmd1.py")], check=True)
        except FileNotFoundError:
            print("❌ Error: sgmd1.py not found!")

    def show_weights(self):
        print("⚖️ Calculating Weights...")
        try:
            subprocess.run(["python3", os.path.abspath("nn1.py")], check=True)
        except FileNotFoundError:
            print("❌ Error: nn1.py not found!")

    def show_predictions(self):
        print("🔮 Running Predictions...")
        try:
            subprocess.run(["python3", os.path.abspath("nn2.py")], check=True)
        except FileNotFoundError:
            print("❌ Error: nn2.py not found!")


# 🔹 Main execution block
if __name__ == "__main__":
    import sys
    print("🚀 Starting the PyQt5 application...")  # Debugging print

    app = QtWidgets.QApplication(sys.argv)
    print("✅ QApplication initialized...")  # Debugging print

    MainWindow = QtWidgets.QMainWindow()
    print("🖥️ Main window created...")  # Debugging print

    ui = Ui_MainWindow()
    print("🔗 UI object created...")  # Debugging print

    ui.setupUi(MainWindow)
    print("✅ UI setup complete...")  # Debugging print

    MainWindow.show()
    print("👀 Showing the window...")  # Debugging print

    sys.exit(app.exec_())  # Keeps the window open
