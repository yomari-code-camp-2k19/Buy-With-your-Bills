import sys
from PyQt5.QtWidgets import QPushButton, QMessageBox, QLineEdit, QLabel
from PyQt5 import QtGui, QtCore, Qt


class IButton(QPushButton):
    def __init__(self):
        super().__init__()

    def addSource(self, source, status="Button"):
        self.source = source
        self.status = status
        self.setIcon(QtGui.QIcon(self.source))
        self.setIconSize(QtCore.QSize(120, 120))
        self.setStatusTip(self.status)
        self.setText(self.status)
        self.setStyleSheet('''background: transparent;
							 border-top: 5px black;
							 border-bottom: 3px ;
							 border-right: 10px ;
							 border-left: 10px ;
							 font: 20px;
							 ''')

    def homeButton(self):
        self.setIcon(QtGui.QIcon("trans.png"))
        self.setIconSize(QtCore.QSize(50, 50))
        self.setStatusTip("Home")
        self.setText("\n" + "Home")
        self.setStyleSheet('''background: transparent;
									 border-top: 3px transparent;
									 border-bottom: 3px transparent;
									 border-right: 10px transparent;
									 border-left: 10px transparent;
									 ''')

    def helpButton(self):
        self.setIcon(QtGui.QIcon("ques.png"))
        self.setIconSize(QtCore.QSize(50, 50))
        self.setStatusTip("Help")
        self.setText("\n" + "About")
        self.setStyleSheet('''background: transparent;
									 border-top: 3px transparent;
									 border-bottom: 3px transparent;
									 border-right: 10px transparent;
									 border-left: 10px transparent;
									 ''')

    def cancelButton(self):
        self.setIcon(QtGui.QIcon("cancel1.jpg"))
        self.setIconSize(QtCore.QSize(50, 50))
        self.setStatusTip("Cancel")
        self.setText("\n" + "Cancel")
        self.setStyleSheet('''background: transparent;
									 border-top: 3px transparent;
									 border-bottom: 3px transparent;
									 border-right: 10px transparent;
									 border-left: 10px transparent;
									 ''')

    def saveButton(self):
        self.setIcon(QtGui.QIcon("ad.png"))
        self.setIconSize(QtCore.QSize(60, 60))
        self.setStatusTip("Save")
        self.setText("\n" + "Save")
        self.setStyleSheet('''background: transparent;
									 border-top: 3px transparent;
									 border-bottom: 3px transparent;
									 border-right: 10px transparent;
									 border-left: 10px transparent;
									 ''')

    def updateButton(self):
        self.setIcon(QtGui.QIcon("update.jpg"))
        self.setIconSize(QtCore.QSize(60, 60))
        self.setStatusTip("Update")
        self.setText("\n" + "")
        self.setStyleSheet('''background: transparent;
								 border-top: 3px transparent;
								 border-bottom: 3px transparent;
								 border-right: 10px transparent;
								 border-left: 10px transparent;
								 ''')

    def issueButton(self):
        self.setIconSize(QtCore.QSize(60, 60))
        self.setStatusTip("Issue")
        self.setText("ISSUE")
        self.setStyleSheet('''background: transparent;
	    				border-top: 3px transparent;
	    				border-bottom: 3px transparent;
	    				border-right: 10px transparent;
	    				border-left: 10px transparent;
	    											 ''')

    def returnButton(self):
        self.setIconSize(QtCore.QSize(60, 60))
        self.setStatusTip("Return")
        self.setText("Return")
        self.setStyleSheet('''background: transparent;
	    				 border-top: 3px transparent;
	    				 border-bottom: 3px transparent;
	    				 border-right: 10px transparent;
	    				 border-left: 10px transparent;
	    				 ''')

    def deleteButton(self):
        self.setIcon(QtGui.QIcon("bin.png"))
        self.setIconSize(QtCore.QSize(60, 60))
        self.setStatusTip("Delete")
        self.setText("\n" + "Delete")
        self.setStyleSheet('''background: transparent;
						 border-top: 3px transparent;
						 border-bottom: 3px transparent;
						 border-right: 10px transparent;
						 border-left: 10px transparent;
						 ''')


class Line(QLineEdit):
    def __init__(self):
        super().__init__()

    def set(self, txt=None, l=400, b=40):
        self.txt = txt
        self.l = l
        self.b = b
        self.setPlaceholderText(self.txt)
        self.setMinimumSize(self.l, self.b)
        self.setStyleSheet("background-color: rgba(225,225,225,0.5);\n"
                           "border-color: rgb(18, 18, 18);"
                           "font: 15pt 'Arial';")


class Label(QLabel):
    def __init__(self):
        super().__init__()
        self.setStyleSheet('''background: transparent;
									 border-top: 3px transparent;
									 border-bottom: 3px transparent;
									 border-right: 10px transparent;
									 border-left: 10px transparent;
									 font: 15pt 'Arial';''')

#
