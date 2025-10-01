
import sys
import os
import subprocess
from PyQt5 import QtWidgets
from bikerental_ui import Ui_MainWindow

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Connect buttons to functions
        self.ui.pushButton.clicked.connect(self.show_traffic_details)
        self.ui.pushButton_2.clicked.connect(self.create_csv)
        self.ui.pushButton_3.clicked.connect(self.show_bike_station_details)
        self.ui.pushButton_4.clicked.connect(self.plot_sigmoid)
        self.ui.pushButton_5.clicked.connect(self.show_weights)
        self.ui.pushButton_6.clicked.connect(self.show_predictions)

    def show_traffic_details(self):
        print("🚦 Opening Traffic Details...")
        try:
            traffic_script = os.path.abspath(os.path.join(os.path.dirname(__file__), "traffic.py"))
            subprocess.run(["python3", traffic_script], check=True)
        except FileNotFoundError:
            print("❌ Error: traffic.py not found!")
        except subprocess.CalledProcessError as e:
            print(f"❌ Error running traffic.py: {e}")

    def create_csv(self):
        print("📁 Creating CSV file...")
        try:
            subprocess.run(["python3", os.path.abspath(os.path.join(os.path.dirname(__file__), "createcsv1.py"))], check=True)
        except FileNotFoundError:
            print("❌ Error: createcsv1.py not found!")

    def show_bike_station_details(self):
        print("🚲 Showing Bike Station Details...")
        try:
            subprocess.run(["python3", os.path.abspath(os.path.join(os.path.dirname(__file__), "bikestn.py"))], check=True)
        except FileNotFoundError:
            print("❌ Error: bikestn.py not found!")

    def plot_sigmoid(self):
        print("📈 Plotting Sigmoid Curve...")
        try:
            subprocess.run(["python3", os.path.abspath(os.path.join(os.path.dirname(__file__), "sgmd1.py"))], check=True)
        except FileNotFoundError:
            print("❌ Error: sgmd1.py not found!")

    def show_weights(self):
        print("⚖️ Calculating Weights...")
        try:
            subprocess.run(["python3", os.path.abspath(os.path.join(os.path.dirname(__file__), "nn1.py"))], check=True)
        except FileNotFoundError:
            print("❌ Error: nn1.py not found!")

    def show_predictions(self):
        print("🔮 Running Predictions...")
        try:
            subprocess.run(["python3", os.path.abspath(os.path.join(os.path.dirname(__file__), "nn2.py"))], check=True)
        except FileNotFoundError:
            print("❌ Error: nn2.py not found!")

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
