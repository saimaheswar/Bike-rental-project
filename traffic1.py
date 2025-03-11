import sys
from traffic import *
from PyQt5 import QtWidgets, QtGui, QtCore
import sqlite3
con = sqlite3.connect('brental1')

class MyForm(QtWidgets.QMainWindow):
  def __init__(self,parent=None):
     QtWidgets.QWidget.__init__(self,parent)
     self.ui = Ui_MainWindow()
     self.ui.setupUi(self)
     self.ui.pushButton.clicked.connect(self.insertvalues) 

   

  def insertvalues(self):
         
     with con:
    
        cur = con.cursor()
        direction1 = str(self.ui.lineEdit_14.text())
        direction2 = str(self.ui.lineEdit_4.text())
        direction3 = str(self.ui.lineEdit_5.text())
        direction4 = str(self.ui.lineEdit_6.text())
        direction5 = str(self.ui.lineEdit_7.text())	
        direction6 = str(self.ui.lineEdit_8.text())
        direction7 = str(self.ui.lineEdit_9.text())
        direction8 = str(self.ui.lineEdit_10.text())
        cur.execute('INSERT INTO traffic VALUES(?,?,?,?,?,?,?,?)',(direction1,direction2,direction3,direction4,direction5,direction6,direction7,direction8))
        con.commit()
        
if __name__ == "__main__":  
    app = QtWidgets.QApplication(sys.argv)
    myapp = MyForm()
    myapp.show()
    sys.exit(app.exec_())


