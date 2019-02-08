import code
import sys
from PyQt5.QtWidgets import (QWidget, QHBoxLayout, QLabel, QGridLayout, QPushButton, QScrollBar, QTableWidget,
                             QVBoxLayout, QMenu,
                             QMainWindow, QTextEdit, QComboBox, QLineEdit, QFormLayout, QTabWidget, QApplication,
                             QAction, QMessageBox, QBoxLayout, QDialog)
from PyQt5 import QtGui, QtCore, Qt, QtWidgets
import sqlite3
import datetime
from store import IButton, Line
import barcode


class App(QMainWindow):
    def __init__(self, title):
        super().__init__()
        self.title = title
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(0, 0, 750, 600)
        self.statusBar().showMessage("Welcome to Store")
        self.setWindowIcon(QtGui.QIcon("library.png"))
        # creating menu
        # self.Menu()

        self.table_widget = MyTableWidget(self)
        self.setCentralWidget(self.table_widget)

        self.show()

    def Menu(self):
        menu = self.menuBar()
        menu.setStyleSheet('''font: 13pt "Arial";''')
        file = menu.addMenu("Main")
        scan = QAction("Scan", self)
        file.addAction(scan)
        image = QAction("Import", self)
        file.addAction(image)
        login = menu.addMenu("Account")
        login.addAction(QAction("Sign Up", self))
        edit = menu.addMenu("About")

        exitButton = QAction(QtGui.QIcon('delete.png'), 'Exit', self)
        exitButton.setShortcut('Ctrl+Q')
        exitButton.setStatusTip('Exit application')
        exitButton.triggered.connect(self.close)
        menu.addAction(exitButton)
        self.show()


class MyTableWidget(QWidget):

    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.layout = QHBoxLayout(self)

        # Initialize tab screen
        self.tabs = QTabWidget()
        self.tab1 = QWidget()
        self.tab1.setStyleSheet(''' background-attachment ="fixed" ''')

        # Add tabs
        self.tabs.addTab(self.tab1, "Home")

        self.Tab3()

        # Create tab layout
        self.layout1 = QVBoxLayout()
        self.layout1.setSpacing(10)

        # Designing layout1 for Home
        self.head1 = QLabel("\tBuy With your Bills", self)
        self.head1.setStyleSheet('color: rgb(200,0, 20);'
                                 'font: bold  25pt "Times New Roman";')

        logbutton = IButton()
        db = sqlite3.connect("store.db")

        for user, mode in db.execute("SELECT * FROM status"):
            if (mode == "loggedin"):
                self.currentUser = user
        print(self.currentUser)
        for balance in db.execute("SELECT Balance FROM user where username = '{}'".format(self.currentUser)):
            print(balance[0])
        db.close()
        logbutton.addSource("adduser.png", "Logged in\n {}\nBalance:{} Dams".format(self.currentUser,balance[0]))
        logbutton.setIconSize(QtCore.QSize(50, 70))
        logbutton.clicked.connect(self.log_clicked)

        scanbutton = IButton()
        scanbutton.addSource("scan.jpg", "Scan")
        scanbutton.clicked.connect(self.scan_click)

        hbox1 = QHBoxLayout()
        hbox1.addWidget(scanbutton)
        hbox1.addStretch(1)
        hbox1.addWidget(self.head1)
        hbox1.addStretch(2)
        hbox1.addWidget(logbutton)
        hbox1.addStretch()

        self.head2 = QLabel("Store", self)
        self.head2.setStyleSheet('color: rgb(25,25,25);' 'font: 20pt "Arial";')

        image = IButton()
        image.addSource("photo.png", "Import")
        image.setIconSize(QtCore.QSize(70, 70))
        image.clicked.connect(self.image_clicked)

        hbox2 = QHBoxLayout()
        hbox2.addWidget(image)
        hbox2.addStretch(2)
        hbox2.addWidget(self.head2)
        hbox2.addStretch(2)

        grid = QGridLayout()

        source = ["books.jpg", "grocery.jpg"]
        img1 = IButton()
        img1.addSource(source[0], "Ebooks")
        grid.addWidget(img1, 0, 0)
        img1.clicked.connect(lambda: self.searchResult("ebook"))
        img2 = IButton()
        img2.addSource(source[1], "Grocery")
        grid.addWidget(img2, 0, 1)
        img2.clicked.connect(lambda: self.searchResult("grocery"))

        Grid = QGridLayout()

        source = ["audio.png", "qfx.png"]
        img1 = IButton()
        img1.addSource(source[0], "Audio")
        Grid.addWidget(img1, 0, 0)
        img1.clicked.connect(lambda: self.searchResult("audio"))
        img2 = IButton()
        img2.addSource(source[1], "QFX Cinemas")
        Grid.addWidget(img2, 0, 1)
        img2.clicked.connect(lambda: self.searchResult("movie"))

        hbox4 = QHBoxLayout()
        hbox4.addStretch(1)
        hbox4.setSpacing(50)
        hbox4.addLayout(grid)
        hbox4.addStretch(1)

        hbox5 = QHBoxLayout()
        hbox5.addStretch(1)
        hbox5.addSpacing(50)
        hbox5.addLayout(Grid)
        hbox5.addStretch(1)

        maker = IButton()
        maker.addSource("User.png", "Designer")
        maker.setText("Sign Up")
        maker.setIconSize(QtCore.QSize(204, 34))
        maker.clicked.connect(self.maker_clicked)
        hbox6 = QHBoxLayout()
        hbox6.addStretch(2)
        hbox6.addWidget(maker)

        self.layout1.addLayout(hbox1)
        self.layout1.addLayout(hbox2)
        self.layout1.addStretch(1)
        self.layout1.addStretch(1)
        self.layout1.addLayout(hbox4)
        self.layout1.addLayout(hbox5)
        self.layout1.addStretch(1)
        self.layout1.addLayout(hbox6)

        self.tab1.setLayout(self.layout1)

        # Add tabs to widget
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)

    def image_clicked(self):
        pass

    def log_clicked(self):
        pass

    def scan_click(self):
        code = barcode.scanQR()
        print(code)
        try:
            db = sqlite3.connect("store.db")
            for c,b,s in db.execute("SELECT Code,balance,status from coupon WHERE Code = {}".format(code)):
                print("Ok")
                if s == "yes":
                    print("fine")
                    for prev in db.execute("Select Balance from user WHERE username = '{}'".format(self.currentUser)):
                        newB = prev[0]+ b
                        print(newB)
                    db.execute("UPDATE user SET Balance = {} WHERE username = '{}'".format(newB, self.currentUser))

                    db.execute("UPDATE coupon SET status = 'No',balance = 0 WHERE Code ={}".format(c))
                    db.commit()
                    db.close()
                    buttonReply = QMessageBox.question(self, 'Recharge Message', "You have recharged {} Dams".format(b),
                                                       QMessageBox.Ok , QMessageBox.Ok)
                    if buttonReply == QMessageBox.Ok:
                        print('Yes clicked.')
                        return 0

                else:
                    print("Here")
                    buttonReply = QMessageBox.question(self, 'Warning', "No Balance available",
                                                       QMessageBox.Ok , QMessageBox.Ok)
                    if buttonReply == QMessageBox.Ok:
                        print('Yes clicked.')
        except:
            buttonReply = QMessageBox.question(self, 'Warning', "Invalid QR",
                                               QMessageBox.Ok, QMessageBox.Ok)
            if buttonReply == QMessageBox.Ok:
                print('Yes clicked.')


    def maker_clicked(self):
        self.Tab2()

    def Tab2(self):
        self.tab2 = QWidget()
        self.tab2.setStyleSheet('''background-image: url("vector10.jpg"); background-attachment ="fixed";
				font: 13pt "Times New Roman";''')
        self.tabs.addTab(self.tab2, "Sign up")

        self.layout2 = QVBoxLayout(self)
        self.layout2.setSpacing(10)

        # Conguring tab2
        head = QLabel("Sign Up your Account", self)
        head.setStyleSheet('color: rgb(25,25,25);' 'font: bold 15pt "Arial";')

        addform = QFormLayout()
        addform.setSpacing(15)

        self.user = Line()
        self.user.set("User name")
        addform.addRow(QLabel("User Name"), self.user)
        self.email = Line()
        self.email.set("Email")
        addform.addRow(QLabel("Email"), self.email)
        self.id = Line()
        self.id.set("CitizenshipNo/passportNo")
        addform.addRow(QLabel("Citizen Id"), self.id)

        h = QHBoxLayout()
        self.yyyy = QtWidgets.QSpinBox()
        self.yyyy.setMinimum(1990)
        self.yyyy.setMaximum(2019)
        self.yyyy.setValue(2010)
        self.month = QComboBox()
        self.month.addItem("Jan")
        self.month.addItem("Feb")
        self.month.addItem("March")
        self.month.addItem("April")
        self.month.addItem("May")
        self.month.addItem("June")
        self.month.addItem("July")
        self.month.addItem("Aug")
        self.month.addItem("Sept")
        self.month.addItem("Oct")
        self.month.addItem("Nov")
        self.month.addItem("Dec")
        self.day = QtWidgets.QSpinBox()
        self.day.setValue(1)
        self.day.setMinimum(1)
        self.day.setMaximum(31)
        h.addWidget(self.yyyy)
        h.addWidget(self.month)
        h.addWidget(self.day)
        addform.addRow(QLabel("Date Of Birth"), h)
        self.dob = "{}-{}-{}".format(self.yyyy.text(), self.month.currentText(), self.day.text())

        self.address = QTextEdit(self)
        self.address.setPlaceholderText("Address")
        addform.addRow(QLabel("Address:"), self.address)

        savebutton = IButton()
        savebutton.saveButton()
        savebutton.clicked.connect(
            lambda: self.save_clicked(self.user.text(), self.email.text(), self.id.text(), self.dob,
                                      self.address.toPlainText()))
        cancelbutton = IButton()
        cancelbutton.cancelButton()
        cancelbutton.clicked.connect(self.cancel_clicked)

        self.homebutton = IButton()
        self.homebutton.homeButton()
        self.homebutton.clicked.connect(self.home_clicked)
        hbx3 = QHBoxLayout()
        hbx3.setSpacing(10)
        hbx3.addWidget(self.homebutton)
        hbx3.addStretch()
        hbx3.addWidget(head)
        hbx3.addStretch()
        hbx3.addWidget(cancelbutton)

        hbx1 = QHBoxLayout()
        hbx1.setSpacing(10)
        hbx1.addStretch(1)
        hbx1.addLayout(addform)
        hbx1.addStretch(2)

        hbx2 = QHBoxLayout()
        hbx2.setSpacing(10)
        hbx2.addStretch(1)
        hbx2.addWidget(savebutton)
        hbx2.addStretch(1)

        self.layout2.addLayout(hbx3)
        self.layout2.addStretch()
        self.layout2.addLayout(hbx1)
        self.layout2.addStretch()
        self.layout2.addLayout(hbx2)
        self.layout2.addStretch()

        self.tab2.setLayout(self.layout2)
        self.tabs.setCurrentWidget(self.tab2)

    def Tab3(self):
        self.tab3 = QWidget()
        self.tab3.setStyleSheet('''background-image: url("abs.jpg"); background-attachment ="fixed";
						font: 15pt "Times New Roman";''')
        self.tabs.addTab(self.tab3, "Help")

        # Designing Help
        layout3 = QVBoxLayout()
        helps = '''\t\tBring us your bill and buy all you want
					Search your favourite Books, review and find the most popular audios and movies here to watch.
				
					Have a GOOD DAY !!!
				'''
        home1 = IButton()
        home1.homeButton()
        home1.clicked.connect(self.home_clicked)
        hb1 = QHBoxLayout()
        hb1.addWidget(home1)
        hb1.addStretch(1)
        layout3.addStretch()
        layout3.addLayout(hb1)
        layout3.addStretch(1)
        layout3.addWidget(QLabel(helps))
        layout3.addStretch(1)

        self.tab3.setLayout(layout3)

    def save_clicked(self, user, email, id, dob, addr):
        if user == '' or email == '' or id == "":
            alert = QMessageBox.question(self, 'Alert message', "User,email and id must be mentioned!!",
                                         QMessageBox.Ok, QMessageBox.Ok)
            if alert == QMessageBox.Ok:
                pass
        else:
            message = QMessageBox.question(self, 'Confirm message', "Do you want to save?",
                                           QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if message == QMessageBox.Yes:
                self.add(user, email, id, dob, addr)

            else:
                pass

    def add(self, user, email, id, dob, addr="",b = 0):
        db = sqlite3.connect("store.db")
        db.execute("""INSERT INTO user(username,email,cid,dob,address,Balance) 
					VALUES('{}','{}','{}','{}','{}','{}')""".format(user, email, id, dob, addr,b))

        db.execute("INSERT INTO status(username,log) VALUES ('{}','loggedoutt')".format(user))
        db.commit()
        db.close()
        self.tabs.currentWidget().deleteLater()

    def on_click(self):
        pass

    def searchResult(self, key):
        self.key = key
        if self.key == "":
            warning = QMessageBox.question(self, "Warning", "Write the words to be searched", QMessageBox.Ok,
                                           QMessageBox.Ok)
        else:
            self.Ebooks = QWidget()
            self.Ebooks.setStyleSheet('''background-image: url("bac1.jpg"); background-attachment ="fixed";
							font: 11pt "Times New Roman";''')

            layout = QVBoxLayout()
            h1 = QHBoxLayout()
            h1.addStretch(2)
            h1.addWidget(QLabel(self.key))
            h1.addStretch(1)
            cancel = IButton()
            cancel.cancelButton()
            cancel.clicked.connect(self.cancel_clicked)
            h1.addWidget(cancel)

            grid = QGridLayout()
            grid.addWidget(QLabel("S.N."), 0, 0)
            grid.addWidget(QLabel("Product"), 0, 1)
            grid.addWidget(QLabel("Category"), 0, 2)
            grid.addWidget(QLabel("Price"), 0, 3)
            grid.addWidget(QLabel("Detail"), 0, 4)

            i = 1

            db = sqlite3.connect("store.db")

            for s, p, c, pr, d in db.execute("SELECT * FROM store WHERE categories ='{}'".format(self.key)):
                print(self.key)
                grid.addWidget(QLabel(str(s)), i, 0)
                grid.addWidget(QLabel(p), i, 1)
                grid.addWidget(QLabel(c), i, 2)
                grid.addWidget(QLabel(str(pr)), i, 3)
                grid.addWidget(QLabel(d), i, 4)
                buy = QPushButton('Buy')
                x = pr
                buy.clicked.connect(lambda checked, x=x: self.buy_clicked(x))
                grid.addWidget(buy, i, 5)
                i += 1
            db.close()
            layout.addLayout(h1)
            layout.addLayout(grid)
            layout.addStretch()

            self.Ebooks.setLayout(layout)
            self.tabs.addTab(self.Ebooks, self.key)
            self.tabs.setCurrentWidget(self.Ebooks)

    def buy_clicked(self, x):
        self.bn = x
        buttonReply = QMessageBox.question(self, 'SOLD', "Do you want to buy?",
                                           QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if buttonReply == QMessageBox.Yes:
            print('Yes clicked.')
        else:
            print('No clicked.')
        db = sqlite3.connect("store.db")
        for prev in db.execute("Select Balance from user WHERE username = '{}'".format(self.currentUser)):
            print(type(prev[0]))
            if(prev[0]< self.bn):
                buttonReply = QMessageBox.question(self, 'Error', "Not enough money",
                                                   QMessageBox.Ok, QMessageBox.Ok)
                if buttonReply == QMessageBox.Ok:
                    print('Yes clicked.')
            else:
                newB = int(prev[0])-int(self.bn)
                print(newB)
                db.execute("UPDATE user SET Balance = {} WHERE username = '{}'".format(newB, self.currentUser))
                db.commit()
                db.close()
                buttonReply = QMessageBox.question(self, 'SOLD', "Sold Successfully",
                                                   QMessageBox.Ok, QMessageBox.Ok)
                if buttonReply == QMessageBox.Ok:
                    print('Yes clicked.')
                    return 0


    def delete_clicked(self):
        pass

    def cancel_clicked(self):
        self.tabs.currentWidget().deleteLater()

    def home_clicked(self):
        self.tabs.setCurrentWidget(self.tab1)

    def help_clicked(self):
        self.tabs.setCurrentWidget(self.tab3)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App("Buy with Bills")
    sys.exit(app.exec())
