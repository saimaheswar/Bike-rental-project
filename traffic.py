# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'traffic.ui'
#
# Created by: PyQt5 UI code generator 5.12.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(483, 395)
        MainWindow.setStyleSheet("color: rgb(0, 0, 255);\n"
                                 "font: 75 12pt \"MS Shell Dlg 2\";")

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(80, 330, 301, 31))
        self.pushButton.setObjectName("pushButton")

        self.lineEdit_4 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_4.setGeometry(QtCore.QRect(430, 80, 21, 33))
        self.lineEdit_4.setObjectName("lineEdit_4")

        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(10, 50, 321, 21))
        self.label_4.setObjectName("label_4")

        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(400, 0, 81, 21))
        self.label_5.setObjectName("label_5")

        self.lineEdit_5 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_5.setGeometry(QtCore.QRect(430, 110, 21, 33))
        self.lineEdit_5.setObjectName("lineEdit_5")

        self.lineEdit_6 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_6.setGeometry(QtCore.QRect(430, 140, 21, 33))
        self.lineEdit_6.setObjectName("lineEdit_6")

        self.lineEdit_7 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_7.setGeometry(QtCore.QRect(430, 170, 21, 33))
        self.lineEdit_7.setObjectName("lineEdit_7")

        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_6.setGeometry(QtCore.QRect(10, 80, 321, 21))
        self.label_6.setObjectName("label_6")

        self.label_7 = QtWidgets.QLabel(self.centralwidget)
        self.label_7.setGeometry(QtCore.QRect(10, 110, 301, 21))
        self.label_7.setObjectName("label_7")

        self.label_8 = QtWidgets.QLabel(self.centralwidget)
        self.label_8.setGeometry(QtCore.QRect(10, 140, 121, 21))
        self.label_8.setObjectName("label_8")

        self.lineEdit_14 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_14.setGeometry(QtCore.QRect(430, 50, 21, 33))
        self.lineEdit_14.setObjectName("lineEdit_14")

        self.label_14 = QtWidgets.QLabel(self.centralwidget)
        self.label_14.setGeometry(QtCore.QRect(10, 0, 361, 41))
        self.label_14.setObjectName("label_14")

        self.label_10 = QtWidgets.QLabel(self.centralwidget)
        self.label_10.setGeometry(QtCore.QRect(10, 170, 251, 21))
        self.label_10.setObjectName("label_10")

        self.lineEdit_8 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_8.setGeometry(QtCore.QRect(430, 200, 21, 33))
        self.lineEdit_8.setObjectName("lineEdit_8")

        self.lineEdit_9 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_9.setGeometry(QtCore.QRect(430, 230, 21, 33))
        self.lineEdit_9.setObjectName("lineEdit_9")

        self.label_11 = QtWidgets.QLabel(self.centralwidget)
        self.label_11.setGeometry(QtCore.QRect(10, 200, 311, 21))
        self.label_11.setObjectName("label_11")

        self.lineEdit_10 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_10.setGeometry(QtCore.QRect(430, 260, 21, 33))
        self.lineEdit_10.setObjectName("lineEdit_10")

        self.label_12 = QtWidgets.QLabel(self.centralwidget)
        self.label_12.setGeometry(QtCore.QRect(10, 230, 141, 21))
        self.label_12.setObjectName("label_12")

        self.label_13 = QtWidgets.QLabel(self.centralwidget)
        self.label_13.setGeometry(QtCore.QRect(10, 260, 311, 21))
        self.label_13.setObjectName("label_13")

        self.label_9 = QtWidgets.QLabel(self.centralwidget)
        self.label_9.setGeometry(QtCore.QRect(400, 20, 51, 21))
        self.label_9.setObjectName("label_9")

        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Traffic Details"))
        self.pushButton.setText(_translate("MainWindow", "Store Traffic Details in Database"))
        self.lineEdit_4.setText(_translate("MainWindow", "N"))
        self.label_4.setText(_translate("MainWindow", "North Direction"))
        self.label_5.setText(_translate("MainWindow", "Abnormal/"))
        self.lineEdit_5.setText(_translate("MainWindow", "N"))
        self.lineEdit_6.setText(_translate("MainWindow", "N"))
        self.lineEdit_7.setText(_translate("MainWindow", "N"))
        self.label_6.setText(_translate("MainWindow", "North East Direction"))
        self.label_7.setText(_translate("MainWindow", "East Direction"))
        self.label_8.setText(_translate("MainWindow", "South East Direction"))
        self.lineEdit_14.setText(_translate("MainWindow", "N"))
        self.label_14.setText(_translate("MainWindow", "Input 'A' if the difference between incoming and\n"
                                                       "outgoing bikes is more than 4, in the next half-an hour"))
        self.label_10.setText(_translate("MainWindow", "South Direction"))
        self.lineEdit_8.setText(_translate("MainWindow", "N"))
        self.lineEdit_9.setText(_translate("MainWindow", "N"))
        self.label_11.setText(_translate("MainWindow", "South West Direction"))
        self.lineEdit_10.setText(_translate("MainWindow", "N"))
        self.label_12.setText(_translate("MainWindow", "West Direction"))
        self.label_13.setText(_translate("MainWindow", "North West Direction"))
        self.label_9.setText(_translate("MainWindow", "Normal"))

# ✅ This part ensures `traffic.py` launches the UI when executed
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
