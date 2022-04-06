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

# file imports

# DB connection
conn = None
try:
    conn = sqlite3.connect('4thYearProject.db')
    # print(sqlite3.version)
except Error as e:
    print(e)

# create users DB
cursor = conn.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS users(ID INTEGER PRIMARY KEY AUTOINCREMENT, username VARCHAR(100) NOT NULL, staffno Varchar(100) NOT NULL, password VARCHAR(100) NOT NULL, email Varchar(100) NOT NULL, phone Varchar(100) NOT NULL,role INT NOT NULL )")
conn.commit()


class Project(auth.Ui_Form, QMainWindow):
    def __init__(self):
        super(Project, self).__init__()
        # setting up the first window
        self.setupUi(self)
        # connect buttons
        self.pushButton.clicked.connect(self.auth)
        self.pushButton_2.clicked.connect(lambda: self.close())

    def auth(self):
        username = self.lineEdit.text()
        password = self.lineEdit_2.text()
        print(username, password)

        # with DBHandler(self.context.get_database) as cursor:

        # create users DB
        cursor = conn.cursor()
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS users(ID INT AUTO_INCREMENT PRIMARY KEY, username VARCHAR(100) NOT NULL, staffno Varchar(100) NOT NULL, password VARCHAR(100) NOT NULL, email Varchar(100) NOT NULL, phone Varchar(100) NOT NULL,role INT NOT NULL )")
        conn.commit()

        find_user_query = """
                SELECT role FROM users WHERE
                username = ? AND password = ?
                """

        cursor.execute(find_user_query, [username, password])

        results = cursor.fetchone()

        try:
            if results[0] == 1:
                print('am here')
                self.ui = Home()
                self.ui.show()
                self.close()

        except TypeError as e:
            # self.error_label.setText(str("Wrong input(s), kindly check your Username and Password. "))
            print(e)


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
        self.bn_close.clicked.connect(self.c)
        self.btn_search.clicked.connect(self.searchVehicle)
        self.bn_min.clicked.connect(self.closeEvent)
        self.bn_max.clicked.connect(lambda: self.showMaximized())
        self.bn_bug.clicked.connect(
            lambda: self.stackedWidget.setCurrentWidget(self.search_registration))
        print(self.search_box.text())
        self.bn_android.clicked.connect(
            lambda: self.stackedWidget.setCurrentWidget(self.page_android)
        )
        # connect buttons
        self.bn_close.clicked.connect(self.c)
        self.btn_search.clicked.connect(self.searchVehicle)
        self.bn_min.clicked.connect(self.closeEvent)
        self.bn_max.clicked.connect(lambda: self.showMaximized())
        self.bn_bug.clicked.connect(
            lambda: self.stackedWidget.setCurrentWidget(self.search_registration))
        self.bn_cloud.clicked.connect(self.showLogs)
        self.bn_home.clicked.connect(
            lambda: self.stackedWidget.setCurrentWidget(self.add_remove_wishlist))
        print(self.search_box.text())
        
        self.bn_android.clicked.connect(
                lambda: self.stackedWidget.setCurrentWidget(
                    self.page_android)
        )

        self.bn_android_contact.clicked.connect(
                lambda: self.stackedWidget_android.setCurrentWidget(
                    self.users_list)
        )
        self.bn_android_game.clicked.connect(
                lambda: self.stackedWidget_android.setCurrentWidget(
                    self.page_android_game)
        )
        self.bn_android_clean.clicked.connect(
                lambda: self.stackedWidget_android.setCurrentWidget(
                    self.page_android_clean)
        )
        self.bn_android_world.clicked.connect(
                lambda: self.stackedWidget_android.setCurrentWidget(
                    self.manage_users)
        )

        # Init QSystemTrayIcon
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(
            self.style().standardIcon(QStyle.SP_ComputerIcon))

        self.bn_android_contact.clicked.connect(
            lambda: self.stackedWidget_android.setCurrentWidget(
                self.users_list)
        )
        self.bn_android_game.clicked.connect(
            lambda: self.stackedWidget_android.setCurrentWidget(
                self.new_user)
        )
        self.bn_android_clean.clicked.connect(
            lambda: self.stackedWidget_android.setCurrentWidget(
                self.page_android_clean)
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
        # Init QSystemTrayIcon
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(
            self.style().standardIcon(QStyle.SP_ComputerIcon))

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
        
    # Override closeEvent, to intercept the window closing event
    # The window will be closed only if there is no check mark in the check box
    def closeEvent(self):
        self.hide()
        self.tray_icon.showMessage(
            "Tray Program",
            "Application was minimized to Tray",
            QSystemTrayIcon.Information,
            2000
        )

    def searchVehicle(self):
        plate = self.search_box.text()
        # print(plate)
        import requests

        try:
            res = requests.get("http://localhost:8000/api/vehicle/"+plate)
            if (res.json() == 'error'):
                # 15 rows
                global l
                l = [['d1', 'l1'], ['d2', 'l2'], ['d3', 'l3'], ['d4', 'l4'], ['d5', 'l5'], ['d6', 'l6'], ['d7', 'l7'], ['d8', 'l8'], [
                    'd9', 'l9'], ['d10', 'l10'], ['d11', 'l11'], ['d12', 'l12'], ['d13', 'l13'], ['d14', 'l14'], ['d15', 'l15']]
                global ct
                ct = 0
                for x in range(0, 15):
                        # 1 columns
                        for y in range(0, 1):
                                self.createNewWidgets(x, y)
                        ct += 1

                def createNewWidgets(self, rowNumber, columnNumber):
                        # create new unique names for each widget
                        newFrame = "frame" + "_" + str(rowNumber)
                        newLabel = "lbl" + "_" + str(rowNumber) 
                        newtEdit = "tEdit" + "_" + str(rowNumber) 
                        print(newFrame, newLabel, newtEdit)

                        self.frame_3 =QFrame(self.scrollAreaWidgetContents_2)
                        self.frame_3.setMinimumSize(QSize(600, 100))
                        self.frame_3.setMaximumSize(QSize(600, 100))
                        self.frame_3.setStyleSheet("background:#0f2027; border-radius: 10px;  border:1px solid #0f2027;")
                        self.frame_3.setFrameShape(QFrame.StyledPanel)
                        self.frame_3.setFrameShadow(QFrame.Raised)
                        self.frame_3.setObjectName(newFrame)
                        self.label_12 = QLabel(self.frame_3)
                        self.label_12.setGeometry(QRect(10, 10, 91, 16))
                        self.label_12.setStyleSheet("background-color: rgb(0, 85, 255); color: rgb(255, 255, 255); border-radius:10px;")
                        self.label_12.setObjectName(newLabel)
                        self.label_12.setText(l[ct][0])
                        self.textEdit = QTextEdit(self.frame_3)
                        self.textEdit.setGeometry(QRect(61, 40, 581, 61))
                        font = QFont()
                        font.setFamily("Arial")
                        font.setPointSize(12)
                        self.textEdit.setFont(font)
                        self.textEdit.setStyleSheet("background:transparent; color:white;")
                        # self.textEdit.setReadOnly(True)
                        self.textEdit.setObjectName(newtEdit)
                        self.textEdit.setText(l[ct] [1])
                        # self.gridLayout_11.addWidget(self.frame_3, 0, 0, 1, 1)

                        # create new attribute to Ui_MainWindow 
                        setattr(self, newFrame, self.frame_3)
                        setattr(self, newLabel, self.frame_3)
                        setattr(self, newtEdit, self.frame_3)
                        self.gridLayout_11.addWidget(self.frame_3, rowNumber, columnNumber, 1, 1)

                # Override closeEvent, to intercept the window closing event
                # The window will be closed only if there is no check mark in the check box
                def closeEvent(self):
                        self.hide()
                        self.tray_icon.showMessage(
                            "ANPR",
                            "The vehicle plate doesn't exist in registered vehicles database.",
                            QSystemTrayIcon.Information,
                            2000
                        )
                        self.lab_tab.setText("Vehicle not found!")
                        timer = QTimer(self)
                        timer.timeout.connect(self.clear_label)
                        timer.start(10000)

            else:
                response = res.json()
                result = response[0]
                # print(result)
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
            print(e)

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
            print('Showing them logs!')
            self.stackedWidget.setCurrentWidget(self.page_logs)
            cursor = conn.cursor()
            cursor.execute("CREATE TABLE IF NOT EXISTS Logs (_id INTEGER, details TEXT, date_recorded DATE);")
            conn.commit()
    # adding car details to carDetails table
    def addCarDetails(self):
        regPlate = self.reg_plate_input.text()
        owner = self.owner_input.text()
        vehicleMake = self.vehicle_make_input.text()
        modelYear = self.year_of_man_input.text()
        engineCapacity = self.engine_capacity_input.text()
        bodyType = self.body_type_input.text()
        color = self.color_input.text()
        logBookNo = self.logbook_number_input.text()
        engineNo = self.engine_number_input.text()
        chasisNo = self.chassis_number_label_2.text()
        watchlist = 0
        # if self.put_on_watchlist.isChecked() == True:
        #     watchlist = 1
        # elif self.remove_from_watchlist.isChecked() == True:
        #     watchlist = 0
        # else:
        #     watchlist = "NULL"
        # print(watchlist)
        # saving data to database
        if regPlate == "" or owner == "" or vehicleMake == "" or modelYear == "" or engineCapacity == "" or bodyType == "" or color == "" or logBookNo == "" or engineNo == "" or chasisNo == "":
            e ="please fill all the fields"
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
      
    #adding user to database       
    def addUser(self):
            name= self.lineEdit.text()
            staffno = self.lineEdit_2.text()
            password = self.lineEdit_3.text()
            confirm_password = self.lineEdit_4.text()
            email = self.lineEdit_5.text()
            phone = self.lineEdit_6.text()
            role = 0
            
            if name=="" or staffno=="" or password=="" or confirm_password=="" or email=="" or phone=="":
                    e ="please fill all the fields"
                    warning_message_box(e)
            elif password != confirm_password:
                    e = "password does not match"
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
                    cursor.execute("""SELECT username, staffno, email, phone FROM users""")
                    result = cursor.fetchall()
                    
                    self.system_users_table.setRowCount(0)
                    for row_number, row_data in enumerate(result):
                        self.system_users_table.insertRow(row_number)
                        for column_number, data in enumerate(row_data):
                            self. system_users_table.setItem(
                                row_number, column_number, QTableWidgetItem(str(data)))
            except Error as e:
                    print(e)
                    
    # print all users
    def printUsers(self):
        pass
                    
    # manage users
    def manageUser(self):
        val = self.lineEdit_13.text()
        if val == "":
            e = "please enter a value"
            warning_message_box(e)
        else:
            try:
                cursor = conn.cursor()
                cursor.execute(
                    """SELECT username, staffno, email,phone,role FROM users WHERE staffno = ?""", (val,))
                data = cursor.fetchall()
            except Error as e:
                warning_message_box(e)
                
    #clearing line edits
    def clearingInputs(self):
        self.lineEdit_7.clear()
        self.lineEdit_8.clear()
        self.lineEdit_9.clear()
        self.lineEdit_11.clear()
        self.lineEdit_12.clear()
                    
                    
# warning message box
def warning_message_box(e):
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Warning)
    msg.setText(e)
    msg.setWindowTitle("Error!")
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
 
if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)
    mw = Home()
    mw.show()
    sys.exit(app.exec())
