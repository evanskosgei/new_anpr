from distutils.log import error
from unittest import result
from urllib.parse import uses_relative
from datetime import date
import calendar
import cffi
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
        self.bn_android_game.clicked.connect(
            lambda: self.stackedWidget_android.setCurrentWidget(
                self.new_user)
        )
        self.bn_android_world.clicked.connect(
            lambda: self.stackedWidget_android.setCurrentWidget(
                self.manage_users)
        )
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
        global cf
        cf = 0
        #1 row
        for x in range(0, 11):
            # 1 columns
            for y in range(0, 1):
                self.camFrame(x, y)
            cf+=1
        
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

    def manageUsers(self):
        if rl == 1:
            self.stackedWidget.setCurrentWidget(self.page_android)
        else:
            self.stackedWidget.setCurrentWidget(self.status_page)
            print("in else" + str(rl))
            self.setIc('./sicon/no_auth.png', 'ERROR!', "You don't have the required permission! Contact the administrator.", 'red', 10000)

    def setIc(self, icn, text, lab_tab_txt, lab_tab_color, lab_tab_timing):
        self.err_ic.setText('<img src="'+icn+'" width="250" height="200">')
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
        print('nmefika hapa')
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
            import requests

            try:
                res = requests.get("http://localhost:8000/api/vehicle/"+plate)
                if (res.json() == 'error'):
                    self.tray_icon.showMessage(
                        "ANPR",
                        "The vehicle not found!",
                        QSystemTrayIcon.Information,
                        2000
                    )
                    self.stackedWidget.setCurrentWidget(self.status_page)
                    self.setIc('./sicon/sorry.ai', 'ERROR!', "The vehicle data requested is ot available", 'red', 10000)

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
                self.setIc('./sicon/net_error.png', 'NETWORK ERROR!', "Network Error!", 'red', 10000)

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
        # print('Showing them logs!')
        self.stackedWidget.setCurrentWidget(self.page_logs)

        try:
            cursor = conn.cursor()
            cursor.execute(
                "CREATE TABLE IF NOT EXISTS Logs (_id INTEGER  PRIMARY KEY AUTOINCREMENT, details TEXT, date_recorded TEXT);")
            conn.commit()
            c = conn.cursor()
            c.execute("SELECT * FROM logs")
            global l
            l = c.fetchall()
            if (len(l) == 0):
                warning_message_box('NO LOGS FOUND')
                self.tray_icon.showMessage(
                    "ANPR",
                    "No logs in the database",
                    QSystemTrayIcon.Information,
                    2000
                )
            else:
                global ct
                ct = 0
                for x in range(0, len(l)):
                    # 1 columns
                    for y in range(0, 1):
                        self.createNewWidgets(x, y)
                    ct += 1
        except Exception as e:
            self.tray_icon.showMessage(
                "DB error",
                "Could NOT sync with database",
                QSystemTrayIcon.Information,
                2000)
    

    def camFrame(self, rNumber, cNumber):
        cFrame = "camframe" + "_" + str(rNumber)
        self.cam_frame = QFrame(self.scrollAreaWidgetContents)
        self.cam_frame.setGeometry(QRect(10, 10, 291, 121))
        self.cam_frame.setMinimumSize(QSize(275, 100))
        self.cam_frame.setMaximumSize(QSize(275, 100))
        self.cam_frame.setFrameShape(QFrame.StyledPanel)
        self.cam_frame.setFrameShadow(QFrame.Raised)
        self.cam_frame.setStyleSheet("background:#0f2027;")
        self.cam_frame.setObjectName(cFrame)
        setattr(self, cFrame, self.cam_frame)
        # self.verticalLayout.addWidget(self.cam_frame)
        # self.gridLayout_11.addWidget(self.frame_3, 0, 0, 1, 1)
        self.gridLayout_6.addWidget(self.cam_frame, rNumber, cNumber, 1, 1)

    def createNewWidgets(self, rowNumber, columnNumber):
        # create new unique names for each widget
        newFrame = "frame" + "_" + str(rowNumber)
        newLabel = "lbl" + "_" + str(rowNumber)
        newtEdit = "tEdit" + "_" + str(rowNumber)
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
        self.label_12.setGeometry(QRect(10, 10, 280, 21))
        self.label_12.setStyleSheet(
            "background-color: rgb(0, 85, 255); color: rgb(255, 255, 255); border-radius:5px;")
        self.label_12.setAlignment(Qt.AlignCenter)
        self.label_12.setObjectName(newLabel)
        self.label_12.setText(l[ct][2])
        self.textEdit = QTextEdit(self.frame_3)
        self.textEdit.setGeometry(QRect(61, 40, 581, 61))
        font = QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        self.textEdit.setFont(font)
        self.textEdit.setStyleSheet("background:transparent; color:white;")
        # self.textEdit.setReadOnly(True)
        self.textEdit.setObjectName(newtEdit)
        self.textEdit.setText(l[ct][1])
        # self.gridLayout_11.addWidget(self.frame_3, 0, 0, 1, 1)

        # create new attribute to Ui_MainWindow
        setattr(self, newFrame, self.frame_3)
        setattr(self, newLabel, self.frame_3)
        setattr(self, newtEdit, self.frame_3)
        self.gridLayout_12.addWidget(
            self.frame_3, rowNumber, columnNumber, 1, 1)
    # print('widgets created')
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
        watchlist = 1
        #searching for an existing car in the database
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT reg_plate FROM carDetails WHERE reg_plate = ?", (regPlate,))
            indata = cursor.fetchall()
        except Error as e:
            warning_message_box(e)
        # saving data to database
        if regPlate == "" or owner == "" or vehicleMake == "" or modelYear == "" or engineCapacity == "" or bodyType == "" or color == "" or logBookNo == "" or engineNo == "" or chasisNo == "":
            e = "please fill all the fields"
            warning_message_box(e)
        elif len(regPlate) < 7:
            e = "Registration Plate number must be 7 characters long"
            warning_message_box(e)
        elif regPlate.isalnum() == False:
            e = "Registration Plate number must be alphanumeric"
            warning_message_box(e)
        elif indata != []:
            e = "Car already exists in the database"
            warning_message_box(e)
        else:
            try:
                cursor = conn.cursor()
                query = """INSERT INTO carDetails(reg_plate, owner, vehicle_make, model_year, engine_capacity, body_type, color, logbook_number, engine_number, chasis_number, watchlist) VALUES(?,?,?,?,?,?,?,?,?,?,?)"""
                data = (regPlate, owner, vehicleMake, modelYear, engineCapacity,
                        bodyType, color, logBookNo, engineNo, chasisNo, watchlist)
                cursor.execute(query, data)
                conn.commit()
                s = "Car details added successfully"
                success_message_box(s)
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
                        "User details have been successfully printed.",
                        QSystemTrayIcon.Information,
                        2000
                    )
                    self.lab_tab.setText("Printed successfully!")
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
        plateno = self.search_box_2.text().upper()
        watchlist = 0
        if plateno == "":
            e = "Fill the empty space"
            warning_message_box(e)
        else:
            try:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM carDetails WHERE reg_plate = ?",(plateno,))
                result = cursor.fetchall()
                if result == []:
                    e = "Such plate number doesnt exist"
                    warning_message_box(e)
                else:
                    for row in result:
                        plate = row[1]
                    try:
                        cursor = conn.cursor()
                        cursor.execute("UPDATE carDetails SET watchlist = ? WHERE reg_plate = ?", (watchlist, plate))
                        conn.commit()
                        s ="updated successfully"
                        success_message_box(s)
                        self.search_box_2.clear()
                    except Error as e:
                        warning_message_box(e)
            except Error as e:
                warning_message_box(e)

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
