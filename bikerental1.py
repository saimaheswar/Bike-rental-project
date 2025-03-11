import sys
import os
from bikerental import *
from PyQt5 import QtWidgets, QtGui, QtCore

class MyForm(QtWidgets.QMainWindow):
  def __init__(self,parent=None):
     QtWidgets.QWidget.__init__(self,parent)
     self.ui = Ui_MainWindow()
     self.ui.setupUi(self)
     self.ui.pushButton.clicked.connect(self.trdtls)
     self.ui.pushButton_2.clicked.connect(self.crcsv)
     self.ui.pushButton_3.clicked.connect(self.bsdtls)
     self.ui.pushButton_4.clicked.connect(self.plsg)
     self.ui.pushButton_5.clicked.connect(self.weights)
     self.ui.pushButton_6.clicked.connect(self.predict)

  def trdtls(self):
    os.system("python traffic1.py")       

  def crcsv(self):
    os.system("python createcsv1.py")

  def bsdtls(self):
    os.system("python bikestn1.py")

  def plsg(self):
    os.system("python sgmd1.py")

  def weights(self):
    os.system("python nn1.py")

  def predict(self):
    os.system("python nn2.py")
     
          
if __name__ == "__main__":  
    app = QtWidgets.QApplication(sys.argv)
    myapp = MyForm()
    myapp.show()
    sys.exit(app.exec_())
