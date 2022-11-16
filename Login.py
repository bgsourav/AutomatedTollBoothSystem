#commands to be typed in mysql/bin before running this program
# initially login as root and then type these commands

# CREATE USER 'Admin'@'%' IDENTIFIED BY '1234';
# GRANT ALL PRIVILEGES ON *.* TO Admin;
# GRANT GRANT OPTION ON *.* TO Admin;
# CREATE USER 'Staff1'@'%' IDENTIFIED BY '1234';


import mysql.connector


def login():
     usernm=input("Enter username (Minimum length is 4): ")
     passwd=input("Enter password: ")
     flag=0
     try:
          if (usernm!="root" and len(usernm)>3 and passwd):
               db = mysql.connector.connect(host ="localhost",
                                        user = usernm,
                                        password = passwd,
                                        db ="tollboothmanagementsystem")
               cursor = db.cursor()
               flag=1
          else:
               print("\nEither USERNAME does not exists or invalid PASSWORD Login failed!\n")
     except mysql.connector.Error as e:
          print(e)
          print("\nCredentials do not match\n")
          return
     if(flag):
          str1='select current_user()'
          cursor.execute(str1)
          res=cursor.fetchone()
          if("Admin@%" in res):
               print("Hello Admin!")
          elif any("Staff" in s for s in res):
               print("Hello Staff")
          else:
               print("Hello customer")
          return db


print("\nWelcome to ATM\n")
print("<Fare details here..>")
ch=input("Do you want to login? [Y/N]\n")
while(ch in ['y','Y']):
     db= login()
     if(db):
          break;
     else:
          ch=input("Would you like to try again? [Y/N]\n")
if (ch in ['N','n']) :
     print("Ok. Thank You!")
