from distutils.log import error
from tkinter import N
from unittest import result
from urllib.parse import uses_relative
from datetime import date
import calendar
import cffi
from matplotlib.cbook import to_filehandle
import home_c as dashboard
import login_c as auth
import bcrypt
from urllib import response
import sys
from sqlite3 import Error
import sqlite3
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtCore import QSize, QTimer
from PyQt5.QtWidgets import *
from turtle import color
import csv
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import random
import requests
from env import *

# DB connection
conn = None
try:
    conn = sqlite3.connect('4thYearProject.db')
    # print(sqlite3.version)
except Error as e:
    print(e)

try:
    # create users DB
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS users(ID INTEGER PRIMARY KEY AUTOINCREMENT, username VARCHAR(100) NOT NULL, staffno Varchar(100) NOT NULL, password VARCHAR(100) NOT NULL, email Varchar(100) NOT NULL, phone Varchar(100) NOT NULL,role INT NOT NULL )")
    conn.commit()
except Error as e:
    print(e)

rl = 'null'

class Project(auth.Ui_Form, QMainWindow):
    def __init__(self):
        super(Project, self).__init__()
        # setting up the first window
        self.setupUi(self)
        # connect buttons
        self.pushButton.clicked.connect(self.auth)
        self.pushButton_2.clicked.connect(lambda: self.close())
        self.label_5.mousePressEvent = self.reset_password

    def auth(self):
        staffno = self.lineEdit.text()
        data = self.lineEdit_2.text()
        try:
            # create users DB
            cursor = conn.cursor()
            cursor.execute(
                "CREATE TABLE IF NOT EXISTS users(ID INT AUTO_INCREMENT PRIMARY KEY, username VARCHAR(100) NOT NULL, staffno Varchar(100) NOT NULL, password VARCHAR(100) NOT NULL, email Varchar(100) NOT NULL, phone Varchar(100) NOT NULL,role INT NOT NULL )")
            conn.commit()
        except Error as e:
            print(e)
        if staffno == "" or data == "":
            print('Please enter your staff number and password')
        else:
            global usr
            usr = staffno
            try:
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT password, role FROM users WHERE staffno = ?", (staffno,))
                result = cursor.fetchall()
                if result == []:
                    e = 'Staff number not found'
                    warning_message_box(e)
                else:
                    for row in result:
                        password = row[0]
                        role = row[1]
                        global rl
                        rl = role
                        print(role)
                    if bcrypt.checkpw(data.encode('utf-8'), password):
                        if role == 1 or role == 2:
                            w = Home()
                            w.lab_user.setText(usr)
                            w.show()
                            self.hide()
                        else:
                            e = "You are not authorised to access this page"
                            warning_message_box(e)
                    else:
                        e = "Incorrect password"
                        warning_message_box(e)
            except Error as e:
                print(e)
                
    # reset password
    def reset_password(self, event):
        staffno = self.lineEdit.text()
        if staffno == "":
            e = "Please enter your staff number"
            warning_message_box(e)
        else:
            try:
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT email, username FROM users WHERE staffno = ?", (staffno,))
                result = cursor.fetchall()
                if result == []:
                    e = 'Staff number not found'
                    warning_message_box(e)
                else:
                    for row in result:
                        email = row[0]
                        name = row[1]
                    #generate random password
                    global passcode
                    code = random.randint(10000, 999999)
                    passcode = name + str(code)
                    #hashing passcode
                    passcode = passcode.encode('utf-8')
                    # generate salt
                    salt = bcrypt.gensalt()
                    # hash password
                    password = bcrypt.hashpw(passcode, salt)
                    # update password
                    try:
                        cursor = conn.cursor()
                        cursor.execute(
                            "UPDATE users SET password = ? WHERE staffno = ?", (password, staffno))
                        conn.commit()
                        
                        self.sendNewPassword(email, str(passcode))
                        s = "Your password has been reset."
                        success_message_box(s)
                    except Error as e:
                        warning_message_box(e)
            except Error as e:
                print(e)
                
    # mail sending
    def sendNewPassword(self, receiver_email, code):
        sender_email = "tyc95182@gmail.com"
        password = "qibtswffxbjcalpu"

        message = MIMEMultipart("alternative")
        # message = "Welcome Home"
        message["Subject"] = "multipart test"
        message["From"] = sender_email
        message["To"] = receiver_email
        
        data = (code.replace(code[0], ''))
        finale = (data.replace(data[0], ''))
        # Create the plain-text and HTML version of your message
        text = """\Your new password is: """ + finale

        # Turn these into plain/html MIMEText objects
        part1 = MIMEText(text, "plain")

        # Add HTML/plain-text parts to MIMEMultipart message
        # The email client will try to render the last part first
        message.attach(part1)

        # Create secure connection with server and send email
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(
                sender_email, receiver_email, message.as_string()
            )
        

class Home(dashboard.Ui_MainWindow, QMainWindow):
    def __init__(self):
        super(Home, self).__init__()
        # setting up the first window
        self.setupUi(self)

        # creating car details table
        try:
            cursor = conn.cursor()
            cursor.execute(
                "CREATE TABLE IF NOT EXISTS carDetails(ID INTEGER PRIMARY KEY AUTOINCREMENT, reg_plate VARCHAR(100) NOT NULL,owner VARCHAR(100) NOT NULL,vehicle_make Varchar(100) NOT NULL,model_year Varchar(100) NOT NULL,engine_capacity Varchar(100) NOT NULL,body_type Varchar(100),color Varchar(100),logbook_number Varchar(100),engine_number Varchar(100),chasis_number Varchar(100),watchlist INT NOT NULL )")
            conn.commit()
        except Error as e:
            print(e)

        # connect buttons
        self.bn_logout.clicked.connect(self.logout)
        self.bn_close.clicked.connect(self.c)
        self.btn_search.clicked.connect(self.searchVehicle)
        self.bn_min.clicked.connect(self.closeEvent)
        self.bn_max.clicked.connect(self.mxmn)
        self.bn_bug.clicked.connect(
            lambda: self.stackedWidget.setCurrentWidget(self.search_registration))
        print(self.search_box.text())
        self.bn_android.clicked.connect(self.manageUsers)
        self.bn_cloud.clicked.connect(self.showLogs)
        self.bn_home.clicked.connect(
            lambda: self.stackedWidget.setCurrentWidget(self.add_remove_wishlist))
        print(self.search_box.text())

        
        self.bn_dashb.clicked.connect(
            lambda: self.stackedWidget.setCurrentWidget(
                self.dashb)
        )

        self.bn_android_contact.clicked.connect(
            lambda: self.stackedWidget_android.setCurrentWidget(
                self.users_list)
        )
        self.bn_android_world.clicked.connect(
            lambda: self.stackedWidget_android.setCurrentWidget(
                self.manage_users)
        )
        self.bn_dw.clicked.connect(
            lambda: self.stackedWidget.setCurrentWidget(
                self.remove_watchlist)
        )

        # Init QSystemTrayIcon
        self.tray_icon = QSystemTrayIcon(self)
        # self.tray_icon.setIcon(
        #     self.style().standardIcon(QStyle.SP_ComputerIcon))
        self.tray_icon.setIcon(QIcon('sicon/logo.png'))

        self.bn_android_contact.clicked.connect(
            lambda: self.stackedWidget_android.setCurrentWidget(
                self.users_list)
        )
        self.view_watchlist.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.watchlist))
        self.bn_android_game.clicked.connect(
            lambda: self.stackedWidget_android.setCurrentWidget(
                self.new_user)
        )
        self.bn_android_world.clicked.connect(
            lambda: self.stackedWidget_android.setCurrentWidget(
                self.manage_users)
        )
        self.pushButton_5.clicked.connect(self.logFilter)
        self.pushButton_6.clicked.connect(self.retrieveCheckboxValues)
        # sending button to db
        self.btn_save_to_wishlist.clicked.connect(self.addCarDetails)
        self.bn_android_contact_save.clicked.connect(self.addUser)
        self.btn_search_2.clicked.connect(self.manageUser)
        # displaying all users
        self.allUsers()
        # updating users
        self.bn_android_contact_edit_2.clicked.connect(self.updateUsers)
        # delete user fro db
        self.bn_android_contact_delete_2.clicked.connect(self.deleteUser)
        # printing data to CSV
        self.bn_android_contact_edit_3.clicked.connect(self.printUsers)
        #Removing from watchlist
        self.btn_search_3.clicked.connect(self.removeWatchlist)
        #
        # global cf
        # cf = 0
        #1 row
        for x in range(0, 2):
            # 1 columns
            for y in range(0, 1):
                self.camFrame(x, y)
            # cf+=1
        
        timer = QTimer(self)
        timer.timeout.connect(self.displayTime)
        timer.start(1000)

        curr_date = date.today()
        self.day_label.setText(calendar.day_name[curr_date.weekday()])
        self.date_label.setText(curr_date.strftime("%d %b %Y"))
        # Init QSystemTrayIcon
        # self.tray_icon = QSystemTrayIcon(self)
        # self.tray_icon.setIcon(
        #     self.style().standardIcon(QStyle.SP_ComputerIcon))

        '''
                    Define and add steps to work with the system tray icon
                    show - show window
                    hide - hide window
                    exit - exit from application
                '''
        show_action = QAction("Show", self)
        quit_action = QAction("Exit", self)
        hide_action = QAction("Hide", self)
        show_action.triggered.connect(self.show)
        hide_action.triggered.connect(self.hide)
        quit_action.triggered.connect(qApp.quit)
        tray_menu = QMenu()
        tray_menu.addAction(show_action)
        tray_menu.addAction(hide_action)
        tray_menu.addAction(quit_action)
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()
        #
        # self.setIc('./sicon/no_auth.png', 'ERROR!', "You don't have the required permission! Contact the administrator ", 'red', 10000)
        #
        global old
        old = 0
        try:
            print(env + "logs")
            o = requests.get(env + "logs")
            old = o.json()
            print("old init " + str(old))
        except Exception as e:
            print("error " + str(e))
            self.tray_icon.showMessage(
                "Tray Program",
                "Network Error. Unable to reach cameras!",
                QSystemTrayIcon.Information,
                2000
            )
            self.stackedWidget.setCurrentWidget(self.status_page)
            icn = './sicon/net_error.png'
            self.setIc('<img src="'+icn+'" width="200" height="200">', 'NETWORK ERROR, UNABLE TO REACH CAMERAS!', "", 'red', 10000)
            warning_message_box("Network Failure, Unable to reach cameras!")
        timer = QTimer(self)
        timer.timeout.connect(self.spotCar)
        timer.start(30000)
        #
        # cur = conn.cursor()
        # cur.execute("SELECT username FROM users WHERE staffno = ?", (usr,))
        # user = cur.fetchone()
        # user_name = user[0]
        # self.label_16.setText("Hello 🙂" + user_name)
        self.label_16.setText("Hello 🙂 ??")
        self.label_17.setText("2 cameras 🎦 active")
        #
        tdy = date.today()
        self.dateEdit_2.setDate(tdy)
        #⬆️init

    def manageUsers(self):
        if rl == 1:
            self.stackedWidget.setCurrentWidget(self.page_android)
        else:
            self.stackedWidget.setCurrentWidget(self.status_page)
            print("in else" + str(rl))
            icn = './sicon/no_auth.png'
            self.setIc('<img src="'+icn+'" width="200" height="200">', 'ERROR!', "You don't have the required permission! Contact the administrator.", 'red', 10000)

    def setIc(self, img, text, lab_tab_txt, lab_tab_color, lab_tab_timing):
        self.err_ic.setText(img)
        self.err_lb.setText(text)
        self.lab_tab.setText(lab_tab_txt)
        self.lab_tab.setStyleSheet("color:" + lab_tab_color)
        timer = QTimer(self)
        timer.timeout.connect(self.clear_label)
        timer.start(lab_tab_timing)

    def showT(self, textdata):
        self.tray_icon.showMessage(
            "ANPR",
            textdata,
            QSystemTrayIcon.Information,
            2000
        )

    def displayTime(self):
        currentTime = QTime.currentTime()
        hours = currentTime.toString('hh')
        minutes = currentTime.toString('mm')
        seconds = currentTime.toString('ss')
        meridiem = currentTime.toString('ap')
        self.am_pm.setText(meridiem.upper())
        self.labelHour.setText(hours)
        self.labelMinute.setText(minutes)
        self.labelSecond.setText(seconds)

    def logout(self):
        self.showT("Logged out successfully")
        self.hide()
        self.tray_icon.hide()
        self.login = Project()
        self.login.show()
        
    def mxmn(self):
        if self.isMaximized():
            self.showNormal()
        else:
            self.showMaximized()

    def closeEvent(self):
        self.hide()
        self.tray_icon.showMessage(
            "Tray Program",
            "Application was minimized to Tray",
            QSystemTrayIcon.error,
            2000
        )

    def searchVehicle(self):
        plate = self.search_box.text()
        # print(plate)
        if (plate == ""):
            e = "Please enter a registration plate"
            warning_message_box(e)
        else:
            try:
                res = requests.get(env + "vehicle/"+plate)
                if (res.json() == 'error'):
                    self.tray_icon.showMessage(
                        "ANPR",
                        "The vehicle not found!",
                        QSystemTrayIcon.Information,
                        2000
                    )
                    self.stackedWidget.setCurrentWidget(self.status_page)
                    icn = './sicon/nodata.png'
                    self.setIc('<img src="'+icn+'" width="250" height="200">', 'SORRY, The vehicle data requested is not available.', "The vehicle data requested is not available", 'red', 10000)

                else:
                    response = res.json()
                    result = response[0]
                    self.tray_icon.showMessage(
                        "ANPR",
                        "Vehicle Details Found.",
                        QSystemTrayIcon.Information,
                        2000
                    )
                    self.lab_tab.setText("Vehicle registration details found!")
                    self.lab_tab.setStyleSheet("color: green")
                    timer = QTimer(self)
                    timer.timeout.connect(self.clear_label)
                    timer.start(10000)
                    # get values from json response
                    try:
                        registration_number = result['registration_number']
                        owner = result['owner']
                        vehicle_make = result['vehicle_make']
                        year_of_manufacture = result['year_of_manufacture']
                        engine_capacity = result['engine_capacity']
                        body_type = result['body_type']
                        color = result['color']
                        logbook_number = result['logbook_number']
                        engine_number = result['engine_number']
                        chassis_number = result['chassis_number']

                    except:
                        print("nop")
                    # set to lineEdit
                    self.reg_plate_input_2.setText(registration_number)
                    self.owner_input_2.setText(owner)
                    self.vehicle_make_input_2.setText(vehicle_make)
                    self.year_of_man_input_2.setText(year_of_manufacture)
                    self.engine_capacity_input_2.setText(engine_capacity)
                    self.body_type_input_2 .setText(body_type)
                    self.color_input_2.setText(color)
                    self.logbook_number_input_2.setText(logbook_number)
                    self.engine_number_input_2.setText(engine_number)
                    self.chassis_number_label_4.setText(chassis_number)
            except Exception as e:
                self.tray_icon.showMessage(
                    "Tray Program",
                    "Network Error!",
                    QSystemTrayIcon.Information,
                    2000
                )
                self.stackedWidget.setCurrentWidget(self.status_page)
                icn = './sicon/no_auth.png'
                self.setIc('<img src="'+icn+'" width="200" height="200">', 'NETWORK ERROR!', "Network Error!", 'red', 10000)

    def c(self):
        self.hide()
        self.tray_icon.showMessage(
            "Tray Program",
            "Application running in background",
            QSystemTrayIcon.Information,
            2000
        )

    def clear_label(self):
        self.lab_tab.clear()

    def showLogs(self):
        self.stackedWidget.setCurrentWidget(self.page_logs)
        try:
            cursor = conn.cursor()
            cursor.execute(
                "CREATE TABLE IF NOT EXISTS Logs (_id INTEGER  PRIMARY KEY AUTOINCREMENT, details TEXT, date_recorded TEXT);")
            conn.commit()
            c = conn.cursor()
            c.execute("SELECT * FROM logs")
            global l
            rs = requests.get(env + "allLogs").json()
            l = rs
            print(l)
            if (len(l) == 0):
                warning_message_box('NO LOGS FOUND')
                self.tray_icon.showMessage(
                    "ANPR",
                    "No logs in the database",
                    QSystemTrayIcon.Information,
                    2000
                )
            else:
                # self.spot_table.setColumnCount(3)
                # self.spot_table.setHorizontalHeaderLabels(['Spotted_plate', 'Highway', 'Date & Time spotted'])
                self.spot_table.setStyleSheet("QHeaderView::section { background-color: #0f2027; color: white;}")
                # # self.spot_table.setStyleSheet("QAbstractItemView {selection-background-color: #1e90ff; selection-color: white;}")
                self.spot_table.setStyleSheet("QAbstractItemView {selection-background-color: #1e90ff; selection-color: white;}")
                self.spot_table.setStyleSheet("QAbstractItemView::indicator {width :35px: height:35px;} QTableWidget::item{width:500px : height:40px}" )
                # self.spot_table.setRowCount(len(l))
                # # self.spot_table.setRowCount(0)
                # for row in range(len(l)):
                #     for col in range(3):
                #         if col % 3 == 0:
                #             item = QTableWidgetItem('Item {0}-{1}'.format(row, col))
                #             item.setFlags(Qt.ItemFlag.ItemIsUserCheckable | Qt.ItemFlag.ItemIsEnabled)
                #             item.setCheckState(Qt.CheckState.Unchecked)
                #             self.spot_table.setItem(row, col, item)
                #         else:
                #             # self.spot_table.setItem(row, col, QTableWidgetItem(l[row][col]))
                #             self.spot_table.setItem(row, col ,QTableWidgetItem('Item {0}-{1}'.format(row, col)))

                self.spot_table.setColumnCount(len(l[0]))
                self.spot_table.setHorizontalHeaderLabels(['Camera ID', 'Spotted_plate', 'Highway', 'Date & Time spotted'])
                self.spot_table.setRowCount(0)
                for row_number, row_data in enumerate(l):
                    self.spot_table.insertRow(row_number)
                    for column_number, data in enumerate(row_data.values()):
                        item = QTableWidgetItem(str(data))
                        if (column_number == 0):
                            item.setFlags(Qt.ItemFlag.ItemIsUserCheckable | Qt.ItemFlag.ItemIsEnabled)
                            item.setCheckState(Qt.CheckState.Unchecked)
                        self. spot_table.setItem(row_number, column_number, item)
        except Exception as e:
            print('error ' + str(e))
            self.tray_icon.showMessage(
                "DB error",
                "Could NOT sync with database",
                QSystemTrayIcon.Information,
                2000)

    def retrieveCheckboxValues(self):
        for row in range(self.spot_table.rowCount()):
            if self.spot_table.item(row, 0).checkState() == Qt.CheckState.Checked:
                ch = [self.spot_table.item(row, col).text() for col in range(self.spot_table.columnCount())]
                print(ch)
                print(ch[1])
                self.spottedVehicle(ch[1])
            

    def logFilter(self):
        fro = self.dateEdit.date().toPyDate()
        to = self.dateEdit_2.date().toPyDate()
        plate = self.lineEdit_10.text()
        print(fro, to, plate)
        try:
            url = env + "logfilter"
            print(url)
            myobj = {'from': str(fro), 'to': str(to), 'plate': plate}
            x = requests.post(url, data = myobj).json()
            # l = x.json()
            # print(l)
            print("len " + str(len(x)))
            self.spot_table.clear()
            self.spot_table.setColumnCount(len(x[0]))
            self.spot_table.setHorizontalHeaderLabels(['Camera ID', 'Spotted_plate', 'Highway', 'Date & Time spotted'])
            self.spot_table.setRowCount(0)
            for row_number, row_data in enumerate(x):
                self.spot_table.insertRow(row_number)
                for column_number, data in enumerate(row_data.values()):
                    item = QTableWidgetItem(str(data))
                    if (column_number == 0):
                        item.setFlags(Qt.ItemFlag.ItemIsUserCheckable | Qt.ItemFlag.ItemIsEnabled)
                        item.setCheckState(Qt.CheckState.Unchecked)
                    self. spot_table.setItem(row_number, column_number, item)
            
        except Exception as e:
            print(e)
            self.tray_icon.showMessage(
                "Tray Program",
                "Logs Filter Failure!",
                QSystemTrayIcon.Information,
                2000
            )
    def deleteAll(self):
        while self.gridLayout_6.count():
            item = self.gridLayout_6.takeAt(0)
            print(item)
            widget = item.widget()
            widget.hide()

    def camFrame(self, rNumber, cNumber):
        cFrame = "camframe" + "_" + str(rNumber)
        newLabel = "lbl" + "_" + str(rNumber)
        newLbl = "lbl" + "_" + str(rNumber)
        newBtn = "btn" + "_" + str(rNumber)
        self.cam_frame = QFrame(self.scrollAreaWidgetContents)
        self.cam_frame.setGeometry(QRect(10, 10, 291, 121))
        self.cam_frame.setMinimumSize(QSize(275, 100))
        self.cam_frame.setMaximumSize(QSize(275, 100))
        self.cam_frame.setFrameShape(QFrame.StyledPanel)
        self.cam_frame.setFrameShadow(QFrame.Raised)
        self.cam_frame.setStyleSheet("background:#0f2027;")
        self.cam_frame.setObjectName(cFrame)
        self.cam_label = QLabel(self.cam_frame)
        self.cam_label.setGeometry(QRect(21, 10, 121, 21))
        self.cam_label.setStyleSheet("background-color: transparent; color: rgb(255, 255, 255); border-radius:5px; font: 75 12pt;")
        self.cam_label.setAlignment(Qt.AlignCenter)
        self.cam_label.setObjectName(newLabel)
        self.cam_label.setText("🎦 CAMERA" + " " + str(rNumber))
        self.cam_lbl = QLabel(self.cam_frame)
        self.cam_lbl.setGeometry(QRect(11, 50, 121, 21))
        self.cam_lbl.setStyleSheet("background-color: transparent; color: rgb(255, 255, 255); border-radius:5px; font: 75 10pt;")
        self.cam_lbl.setAlignment(Qt.AlignCenter)
        self.cam_lbl.setObjectName(newLbl)
        self.cam_lbl.setText("📌 HIGHWAY " + " " + str(rNumber))
        self.cam_btn = QPushButton(self.cam_frame)
        self.cam_btn.setGeometry(QRect(175, 70, 65, 21))
        self.cam_btn.setStyleSheet("background-color: #EE8A09; color: black; border-radius:5px; font: 75 8pt;")
        self.cam_btn.setCursor(QCursor(Qt.PointingHandCursor))
        self.cam_btn.clicked.connect(lambda : print(newBtn + " was clicked."))
        self.cam_btn.setObjectName(newBtn)
        self.cam_btn.setText("DETAILS ➡️")
        #set attributes
        setattr(self, cFrame, self.cam_frame)
        setattr(self, newLabel, self.cam_frame)
        setattr(self, newBtn, self.cam_frame)
        self.gridLayout_6.addWidget(self.cam_frame, rNumber, cNumber, 1, 1)

    def createNewWidgets(self, rowNumber, columnNumber):
        ct = 0
        # create new unique names for each widget
        newFrame = "frame" + "_" + str(rowNumber)
        newLabel = "lbl" + "_" + str(rowNumber)
        newtEdit = "tEdit" + "_" + str(rowNumber)
        newBn = "bt" + "_" + str(rowNumber)
        # print(newFrame, newLabel, newtEdit)

        self.frame_3 = QFrame(self.scrollAreaWidgetContents_2)
        self.frame_3.setMinimumSize(QSize(600, 100))
        self.frame_3.setMaximumSize(QSize(600, 100))
        self.frame_3.setStyleSheet(
            "background:#0f2027; border-radius: 10px;  border:1px solid #0f2027;")
        self.frame_3.setFrameShape(QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QFrame.Raised)
        self.frame_3.setObjectName(newFrame)
        self.label_12 = QLabel(self.frame_3)
        self.label_12.setGeometry(QRect(10, 10, 210, 21))
        self.label_12.setStyleSheet(
            "background-color: rgb(0, 85, 255); color: rgb(255, 255, 255); border-radius:5px;font: 75 10pt;")
        self.label_12.setAlignment(Qt.AlignLeft)
        self.label_12.setObjectName(newLabel)
        self.label_12.setText("📅 " + l[ct]['created_at'])
        self.textEdit = QTextEdit(self.frame_3)
        self.textEdit.setGeometry(QRect(61, 40, 581, 61))
        font = QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        self.textEdit.setFont(font)
        self.textEdit.setStyleSheet("background:transparent; color:white;")
        # self.textEdit.setReadOnly(True)
        self.textEdit.setObjectName(newtEdit)
        self.textEdit.setText(l[ct]['spotted_plate'])
        sp = l[ct]['spotted_plate']
        self.lg_btn = QPushButton(self.frame_3)
        self.lg_btn.setGeometry(QRect(475, 70, 95, 21))
        self.lg_btn.setStyleSheet("background-color: #EE8A09; color: black; border-radius:5px; font: 75 8pt;")
        self.lg_btn.setCursor(QCursor(Qt.PointingHandCursor))
        self.lg_btn.clicked.connect(lambda : self.spottedVehicle(sp))
        self.lg_btn.setObjectName(newBn)
        self.lg_btn.setText("MORE DETAILS ➡️")
        # create new attribute to Ui_MainWindow
        setattr(self, newFrame, self.frame_3)
        setattr(self, newLabel, self.frame_3)
        setattr(self, newtEdit, self.frame_3)
        setattr(self, newBn, self.frame_3)
        self.gridLayout_15.addWidget(self.frame_3, rowNumber, columnNumber, 1, 1)

    def spottedVehicle(self, sp):
        print('sp ' + sp)
        self.stackedWidget.setCurrentWidget(self.spotted_vehicles)
        plate = sp
        try:
            res = requests.get(env + "vehicle/"+plate)
            if (res.json() == 'error'):
                self.tray_icon.showMessage(
                    "ANPR",
                    "The vehicle not found!",
                    QSystemTrayIcon.Information,
                    2000
                )
                self.stackedWidget.setCurrentWidget(self.status_page)
                icn = './sicon/nodata.png'
                self.setIc('<img src="'+icn+'" width="250" height="200">', 'SORRY, The vehicle data requested is not available.', "The vehicle data requested is not available", 'red', 10000)

            else:
                response = res.json()
                result = response[0]
                self.tray_icon.showMessage(
                    "ANPR",
                    "Vehicle Details Found.",
                    QSystemTrayIcon.Information,
                    2000
                )
                self.lab_tab.setText("Vehicle registration details found!")
                self.lab_tab.setStyleSheet("color: green")
                timer = QTimer(self)
                timer.timeout.connect(self.clear_label)
                timer.start(10000)
                # get values from json response
                try:
                    registration_number = result['registration_number']
                    owner = result['owner']
                    vehicle_make = result['vehicle_make']
                    year_of_manufacture = result['year_of_manufacture']
                    engine_capacity = result['engine_capacity']
                    body_type = result['body_type']
                    color = result['color']
                    logbook_number = result['logbook_number']
                    engine_number = result['engine_number']
                    chassis_number = result['chassis_number']

                except:
                    print("nop")
                # set to lineEdit
                self.reg_plate_input_3.setText(registration_number)
                self.owner_input_3.setText(owner)
                self.vehicle_make_input_3.setText(vehicle_make)
                self.year_of_man_input_3.setText(year_of_manufacture)
                self.engine_capacity_input_3.setText(engine_capacity)
                self.body_type_input_3.setText(body_type)
                self.color_input_3.setText(color)
                self.logbook_number_input_3.setText(logbook_number)
                self.engine_number_input_3.setText(engine_number)
                self.chassis_number_label_6.setText(chassis_number)
        except Exception as e:
            self.tray_icon.showMessage(
                "Tray Program",
                "Network Error!",
                QSystemTrayIcon.Information,
                2000
            )
            self.stackedWidget.setCurrentWidget(self.status_page)
            icn = './sicon/no_auth.png'
            self.setIc('<img src="'+icn+'" width="200" height="200">', 'SORRY,NETWORK ERROR. UNABLE TO SEARCH FOR THE SPOTTED CAR DETAILS!', "Network Error!", 'red', 10000)



    def spotCar(self):
        #get no of logs in db
        global old
        old = old
        plate="SAMPLE"
        try:
            res = requests.get(env + "logs")
            n = res.json()
            print("...n " + str(res.json()))
            if (n > old):
                print("...old " + str(old))
                self.tray_icon.showMessage(
                    "Tray Program",
                    "Vehicle " + plate + " has been spotted!",
                    QSystemTrayIcon.Information,
                    2000
                )
                old = n
        
        except Exception as e:
            print("error... " + str(e))
            self.tray_icon.showMessage(
                "Tray Program",
                "Network Error. Unable to reach cameras!",
                QSystemTrayIcon.Information,
                2000
            )
            warning_message_box("Network Failure, Unable to reach cameras!")
            timer = QTimer(self)
            timer.timeout.connect(self.clear_label)
            timer.start(10000)
        print("old reassigned " + str(old))
        
    # adding car details to carDetails table
    def addCarDetails(self):
        regPlate = self.reg_plate_input.text().upper()
        owner = self.owner_input.text()
        vehicleMake = self.vehicle_make_input.text()
        modelYear = self.year_of_man_input.text()
        engineCapacity = self.engine_capacity_input.text()
        bodyType = self.body_type_input.text()
        color = self.color_input.text()
        logBookNo = self.logbook_number_input.text()
        engineNo = self.engine_number_input.text()
        chasisNo = self.chassis_number_label_2.text()
        
        #searching for an existing car in the database
        # try:
        #     cursor = conn.cursor()
        #     cursor.execute("SELECT reg_plate FROM carDetails WHERE reg_plate = ?", (regPlate,))
        #     indata = cursor.fetchall()
        # except Error as e:
        #     warning_message_box(e)
        # saving data to database
        # print("reached here")
        if regPlate == "" or vehicleMake == "" or color =="":
            e = "A registration plate, vehicle make and color is mandatory!"
            warning_message_box(e)
        if owner == "":
            owner = "none provided"
        if modelYear == "":
            modelYear = "none provided"
        if engineCapacity == "":
            engineCapacity = "none provided"
        if bodyType == "":
            bodyType = "none provided"
        if logBookNo == "":
            logBookNo = "none provided"
        if engineNo == "":
            engineNo = "none provided"
        if chasisNo == "":
            chasisNo = "none provided"
        elif len(regPlate) < 7:
            e = "Registration Plate number must be 7 characters long"
            warning_message_box(e)
        
        # elif indata != []:
        #     e = "Car already exists in the database"
        #     warning_message_box(e)
        else:
            print("add to watchlist ERROR!")
        try:
            # cursor = conn.cursor()
            # query = """INSERT INTO carDetails(reg_plate, owner, vehicle_make, model_year, engine_capacity, body_type, color, logbook_number, engine_number, chasis_number, watchlist) VALUES(?,?,?,?,?,?,?,?,?,?,?)"""
            # data = (regPlate, owner, vehicleMake, modelYear, engineCapacity,
            #         bodyType, color, logBookNo, engineNo, chasisNo, watchlist)
            # cursor.execute(query, data)
            # conn.commit()
            try:
                url = env + "add_to_watchlist"
                print(url)
                myobj = {'reg_plate': regPlate, 'owner': owner, 'vehicle_make': vehicleMake, 'model_year': modelYear, 
                'engine_capacity': engineCapacity, 'body_type': bodyType, 'color': color, 'logbook_number': logBookNo,
                'engine_number': engineNo, 'chasis_number': chasisNo}
                # print(regPlate, owner, vehicleMake, modelYear, engineCapacity, bodyType, color, logBookNo, engineNo, chasisNo)
                x = requests.post(url, data = myobj)
                print(x.json())
                if x.json() == "success":
                    s = "Car details added successfully"
                    self.lab_tab.setText("Vehicle plate added to watchlist successfully!")
                    self.lab_tab.setStyleSheet("color: green")
                    timer = QTimer(self)
                    timer.timeout.connect(self.clear_label)
                    timer.start(10000)
                    success_message_box(s)
                else:
                    s = "Failed to add car details"
                    self.lab_tab.setText("Failed to add car details")
                    self.lab_tab.setStyleSheet("color: red")
                    timer = QTimer(self)
                    timer.timeout.connect(self.clear_label)
                    timer.start(10000)
                    warning_message_box(s)
            except Exception as e:
                print("ERROR!" + str(e))
        except Error as e:
            warning_message_box(e)
        self.clearLogs()

    def clearLogs(self):
        self.reg_plate_input.clear()
        self.owner_input.clear()
        self.vehicle_make_input.clear()
        self.year_of_man_input.clear()
        self.engine_capacity_input.clear()
        self.body_type_input.clear()
        self.color_input.clear()
        self.logbook_number_input.clear()
        self.engine_number_input.clear()
        self.chassis_number_label_2.clear()

    def clear_label(self):
        self.lab_tab.clear()
        
    # adding user to database
    def addUser(self):
        name = self.lineEdit.text()
        staffno = self.lineEdit_2.text()
        password = self.lineEdit_3.text()
        confirm_password = self.lineEdit_4.text()
        email = self.lineEdit_5.text()
        phone = self.lineEdit_6.text()
        role = 2 
        #selecting users from db
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT staffno, email FROM users WHERE staffno = ? OR email = ?", (staffno, email))
            indata = cursor.fetchall()
        except error as e:
            print(e)       
        if name == "" or staffno == "" or password == "" or confirm_password == "" or email == "" or phone == "":
            e = "please fill all the fields"
            warning_message_box(e)
        elif indata != []:
            e = "Staff number or email already exists"
            warning_message_box(e)
        elif password != confirm_password:
            e = "password does not match"
            warning_message_box(e)
        elif len(password) < 8:
            e = "Atleast 8 characters for your password"
            warning_message_box(e)
        elif "@" not in email:
            e = "Invalid email"
            warning_message_box(e)
        elif ".com" not in email:
            e = "Invalid email"
            warning_message_box(e)
        elif len(phone) < 10:
            e = "Invalid phone number. Atleast 10 digits needed"
            warning_message_box(e)
        else:
            password = password.encode('utf-8')
            # generate salt
            salt = bcrypt.gensalt()
            # hash password
            hash = bcrypt.hashpw(password, salt)
            try:
                cursor = conn.cursor()
                query = """INSERT INTO users(username, staffno, password, email, phone,role) VALUES(?,?,?,?,?,?)"""
                data = (name, staffno, hash, email, phone, role)
                cursor.execute(query, data)
                conn.commit()
                s = "user added successfully"
                success_message_box(s)
            except Error as e:
                warning_message_box(e)

            self.lineEdit.clear()
            self.lineEdit_2.clear()
            self.lineEdit_3.clear()
            self.lineEdit_4.clear()
            self.lineEdit_5.clear()
            self.lineEdit_6.clear()

    # # display all users
    def allUsers(self):
        try:
            cursor = conn.cursor()
            cursor.execute(
                """SELECT username, staffno, email, phone,role FROM users""")
            result = cursor.fetchall()
            if result == []:
                e = "No users found in database"
                warning_message_box(e)
            else:
                self.system_users_table.setColumnCount(5)
                self.system_users_table.setHorizontalHeaderLabels(
                    ['Username', 'Staff Number', 'Email', 'Phone', 'Role'])
                self.system_users_table.setRowCount(0)
                for row_number, row_data in enumerate(result):
                    self.system_users_table.insertRow(row_number)
                    for column_number, data in enumerate(row_data):
                        self. system_users_table.setItem(
                            row_number, column_number, QTableWidgetItem(str(data)))
        except Error as e:
            warning_message_box(e)

    # print all users
    def printUsers(self):
        print("Printing users")
        try:
            cursor = conn.cursor()
            cursor.execute(
                """SELECT username, staffno, email, phone, role FROM users""")
            result = cursor.fetchall()
            if result == []:
                e = "No users found in database"
                warning_message_box(e)
            else:
                with open('users.csv', 'w', newline='') as csvfile:
                    fieldnames = ['Username', 'Staff Number',
                                'Email', 'Phone', 'Role']
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                    writer.writeheader()
                    for row_data in result:
                        writer.writerow({'Username': row_data[0], 'Staff Number': row_data[1],
                                        'Email': row_data[2], 'Phone': row_data[3], 'Role': row_data[4]})

                    self.tray_icon.showMessage(
                        "ANPR",
                        "Downloaded successfully, to your documents folder",
                        QSystemTrayIcon.Information,
                        2000
                    )
                    self.lab_tab.setText("Downloaded successfully!")
                    self.lab_tab.setStyleSheet("color: green")
                    timer = QTimer(self)
                    timer.timeout.connect(self.clear_label)
                    timer.start(10000)

        except Error as e:
            warning_message_box(e)

    # manage users
    def manageUser(self):
        val = self.lineEdit_13.text()
        if val == "":
            e = "please enter a value"
            warning_message_box(e)
        else:

            if self.radioButton_5.isChecked() == True:
                try:
                    cursor = conn.cursor()
                    cursor.execute(
                        """SELECT username, staffno, email, phone, role FROM users WHERE staffno = ?""", (val,))
                    data = cursor.fetchall()
                    if data == []:
                        e = "user not found"
                        warning_message_box(e)
                    else:
                        global item
                        for item in data:
                            item
                        self.assignLineEdits()
                        self.lineEdit_13.clear()
                except Error as e:
                    warning_message_box(e)

            elif self.radioButton_6.isChecked() == True:
                try:
                    cursor = conn.cursor()
                    cursor.execute(
                        """SELECT username, staffno, email, phone, role FROM users WHERE email = ?""", (val,))
                    data = cursor.fetchall()
                    if data == []:
                        e = "user not found"
                        warning_message_box(e)
                    else:
                        for item in data:
                            item
                        self.assignLineEdits()
                        self.lineEdit_13.clear()
                except Error as e:
                    warning_message_box(e)
            else:
                e = "please select a value from the radio buttons"
                warning_message_box(e)

    # updating function for users
    def updateUsers(self):
        name = self.lineEdit_7.text()
        staffno = self.lineEdit_8.text()
        role = self.lineEdit_9.text()
        email = self.lineEdit_11.text()
        phone = self.lineEdit_12.text()

        if name == "" or staffno == "" or role == "" or email == "" or phone == "":
            e = "Please search for the user first before updating!"
            warning_message_box(e)

        elif "@" not in email:
            e = "Invalid email"
            warning_message_box(e)
        elif ".com" not in email:
            e = "Invalid email"
            warning_message_box(e)
        elif len(phone) < 10:
            e = "Invalid phone number. Atleast 10 digits needed"
            warning_message_box(e)
        else:
            try:
                cursor = conn.cursor()
                cursor.execute(
                    """UPDATE users SET role = ?, email = ?, phone = ? WHERE staffno = ?""", (role, email, phone, staffno))
                conn.commit()
                s = "user details updated successfully"
                text = "Your details have been successfully updated by the system administrator"
                self.sendEmail(text, email)
                success_message_box(s)
                self.clearingInputs()

            except Error as e:
                warning_message_box(e)

    # sending email to users
    def sendEmail(self, text, receiver_email):
        sender_email = "tyc95182@gmail.com"
        password = "qibtswffxbjcalpu"

        message = MIMEMultipart("alternative")
        # message = "Welcome Home"
        message["Subject"] = "multipart test"
        message["From"] = sender_email
        message["To"] = receiver_email

        # Create the plain-text and HTML version of your message
        text = text
        # """\
        # ALERT,
        # HELP!
        # Your details have been updated by the system administrator.:
        # www.realpython.html"""
        # html = """\
        # <html>
        # <body>
        #     <p>ALERT,<br>
        #     HELP!<br>
        #     <a href="http://www.realpython.html">Your details have been updated </a>
        #     by the system administrator.
        #     </p>
        # </body>
        # </html>
        # """

        # Turn these into plain/html MIMEText objects
        part1 = MIMEText(text, "plain")
        # part2 = MIMEText(html, "html")

        # Add HTML/plain-text parts to MIMEMultipart message
        # The email client will try to render the last part first
        message.attach(part1)
        # message.attach(part2)

        # Create secure connection with server and send email
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(
                sender_email, receiver_email, message.as_string()
            )

    # deleting user
    def deleteUser(self):
        staffno = self.lineEdit_8.text()

        if staffno == "":
            e = "Please search for the user first before deleting!"
            warning_message_box(e)
        else:
            a = "Are you sure you want to delete this user?"
            areYouSure(a)
            try:
                cursor = conn.cursor()
                cursor.execute(
                    """DELETE FROM users WHERE staffno = ?""", (staffno,))
                conn.commit()
                s = "user deleted successfully"
                success_message_box(s)
                self.clearingInputs()
            except Error as e:
                warning_message_box(e)
    # clearing line edits

    def clearingInputs(self):
        self.lineEdit_7.clear()
        self.lineEdit_8.clear()
        self.lineEdit_9.clear()
        self.lineEdit_11.clear()
        self.lineEdit_12.clear()

    # assigning values to line edits
    def assignLineEdits(self):
        self.lineEdit_7.setText(str(item[0]))
        self.lineEdit_8.setText(str(item[1]))
        self.lineEdit_9.setText(str(item[4]))
        self.lineEdit_11.setText(str(item[2]))
        self.lineEdit_12.setText(str(item[3]))
        
    #Remove from watchlist
    def removeWatchlist(self):
        plateno = self.search_box_2.text()
        print(plateno)
        if plateno == "":
            e = "Fill the empty space"
            warning_message_box(e)
        else:
            try:
                res = requests.get(env + "delete_from_watchlist/" + plateno)
                print(res.json())
                if res.json() == "success":
                    self.lab_tab.setText("Vehicle plate removed from watchlist successully!")
                    self.lab_tab.setStyleSheet("color: green")
                    timer = QTimer(self)
                    timer.timeout.connect(self.clear_label)
                    timer.start(10000)
                    self.tray_icon.showMessage(
                    "Tray Program",
                    "Vehicle plate removed from watchlist successully!",
                    QSystemTrayIcon.Information,
                    2000
                )
                else:
                    self.lab_tab.setText("Error occured! The plate entered was not on the watchlist")
                    self.lab_tab.setStyleSheet("color: red")
                    timer = QTimer(self)
                    timer.timeout.connect(self.clear_label)
                    timer.start(10000)
                    self.tray_icon.showMessage(
                    "Tray Program",
                    "Error occured! The plate entered was not on the watchlist",
                    QSystemTrayIcon.Information,
                    2000
                )
            except Exception as e:
                print(e)

# warning message box
def warning_message_box(e):
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Warning)
    msg.setText(e)
    msg.setWindowTitle("Warning!")
    msg.setStandardButtons(QMessageBox.Ok)
    msg.exec_()

# success message box
def success_message_box(s):
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Information)
    msg.setText(s)
    msg.setWindowTitle("Success!")
    msg.setStandardButtons(QMessageBox.Ok)
    msg.exec_()

# critical message box
def areYouSure(a):
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Critical)
    msg.setText(a)
    msg.setWindowTitle("Are you sure?")
    msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
    msg.exec_()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)
    mw = Project()
    mw.show()
    sys.exit(app.exec())
