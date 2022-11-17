#commands to be typed in mysql/bin before running this program
# initially login as root and then type these commands

# CREATE USER 'Admin'@'%' IDENTIFIED BY '1234';
# GRANT ALL PRIVILEGES ON *.* TO Admin;
# GRANT GRANT OPTION ON *.* TO Admin;
# CREATE USER 'Staff1'@'%' IDENTIFIED BY '1234';


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
          print(res)
          if("ADMIN01@%" in res or "ADMIN02@%" in res):
               print("Logged in as Admin..")
          else:
               print("Logged in as Staff..")
          return db


def car_entered(db,mycursor):
     reg_no=input("Please Enter the car Registration number : ")
     str1=f"select * from vehicle_Details where Registration_number= '{reg_no}'"
     mycursor.execute(str1)
     res1=mycursor.fetchone()
     if(res1):      #if car is present in database
          car_present(db,mycursor,reg_no)
     # else:        #if car is not present in database
     #      car_notpresent(db,mycursor,reg_no)

def car_present(db,mycursor,reg_no):
     str1=f"Select check_flag from vehicle_details where check_flag=2 and Registration_Number = '{reg_no}'"
     mycursor.execute(str1)
     str1=mycursor.fetchone()
     if (str1):
          print("This is a government vehicle and is exempted from tax..")
          return
     toll_no=int(input(("Please enter the toll booth number where the vehicle entered")))
     str2=f"Select Toll_Booth_No from Toll_Booth where Toll_Booth_No={toll_no}"
     mycursor.execute(str2)
     str2=mycursor.fetchone()
     if(str2==0):   #balance is less than fare
          # ask passenger to add money to account
          print("Your account balance is low..")
          balanc=f"select distinct balance from Transaction_Details natural join Vehicle_Details natural join Account_Details where Vehicle_Details.Registration_Number='{reg_no}'"
          mycursor.execute(balanc)      #get balance 
          balanc=mycursor.fetchone()
          print("Balance : ",balanc)
          faree=f"select Toll_Price from Fare_Table natural join Vehicle_Details where Vehicle_Details.Registration_Number={reg_no}"
          mycursor.execute(faree)       #get toll price
          faree=mycursor.fetchone()
          print("Please recharge now.")
          recharg=int(input(f"Enter the recharge amount (Minimum amount : {faree}). "))
          while(recharg<faree):
               print("Please enter minimum amount")
               recharg=int(input(f"Enter the recharge amount (Minimum amount : {faree}). "))
          balanc+=recharg-faree
          print("Recharge successful..")
          str3=f"UPDATE Account_Details natural JOIN Transaction_Details SET Account_Details.balance = {balanc} WHERE Transaction_Details.Registration_Number = '{reg_no}'"
          mycursor.execute(str3)       #update the balance 
          print("Tax deducted sucessfully..\n Balance amount has been updated")
          print("Balance amount : ",balanc)
     #      if (balanc>faree):          #check if newbalance is low
               
     # else:
     #      pass

     

# def car_enter(db):
#      #enter car details
     #  ask for tolbooth numbr
#      check for it in car details table
#      if present:
#           check bit:
#                deduct balance
#           else if:
#                set check bit to 0
#                give Warning
#                ask for payemnt
#           else:
#                leave without tax for govt vehicles
#           update transac details
#           update toll booth revenue
#           if balance_new > fare:
#                update check bit
#      else:
#           insert into car details table
#           ask payment
#           insert into transac
#           if balance_new > fare:
#                update check bit


              
