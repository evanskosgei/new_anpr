# seed user to the database
from optparse import Values
from unittest import result
import bcrypt
import sqlite3

from colorama import Cursor

# DB connection
conn = None
try:
    conn = sqlite3.connect('4thYearProject.db')
    # print(sqlite3.version)
except Exception as e:
    print(e)

username = 'Admin'
staffno = 'AD3'
code = 'Admin12345'
email = 'studioskanga@gmail.com'
phone = '+639123456789'
role = '1'

#hashing passcode
passcode = code.encode('utf-8')
# generate salt
salt = bcrypt.gensalt()
# hash password
password = bcrypt.hashpw(passcode, salt)
try:
    Cursor = conn.cursor()
    Cursor.execute("SELECT * FROM users WHERE staffno = ?", (staffno,))
    result = Cursor.fetchone()
    if result is None:
        Cursor.execute("INSERT INTO users (username, staffno, password, email, phone, role) VALUES (?, ?, ?, ?, ?, ?)", (username, staffno, password, email, phone, role))
        conn.commit()
except Exception as e:
    print(e)