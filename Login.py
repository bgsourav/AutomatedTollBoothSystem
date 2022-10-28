#commands to be typed in mysql/bin before running this program
# initially login as root and then type these commands

# CREATE USER 'Admin'@'%' IDENTIFIED BY '1234';
# GRANT ALL PRIVILEGES ON *.* TO Admin;
# CREATE USER 'Staff1'@'%' IDENTIFIED BY '1234';


import mysql.connector
import tkinter

# mydb=mysql.connector.connect(
#      host = "localhost",
#      user = "root",
#      database = "tollboothmanagementsystem"
# )
# mycursor = mydb.cursor()

def login(usernm,passwd):
     if (usernm!="root" and passwd):
          db = mysql.connector.connect(host ="localhost",
                                     user = usernm,
                                     password = passwd,
                                     db ="tollboothmanagementsystem")
          cursor = db.cursor()
     str1='select current_user()'
     if("Admin@%" in cursor.fetchone()):
          print("Hello Admin!")
     elif any("Staff" in cursor.fetchone()):
          print("Hello Staff")
     else:
          print("Hello user")


print("Welcome to ATM\n")
ch=input("Do you want to login? \n")
if(ch=='y'):
     usrname=input("Enter name: ")
     passwd=input("Enter password: ")
     login(usrname,passwd)

     