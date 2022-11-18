import mysql.connector


def login():
     usernm=input("Enter username (Minimum length is 4): ")
     passwd=input("Enter password: ")
     flag=0
     try:
          if (usernm!="root" and len(usernm)>3 and passwd):           #must not login as root
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
          str1='select current_user()'            #gives the name of the loged in account
          cursor.execute(str1)
          res=cursor.fetchone()
          if("ADMIN01@%" in res or "ADMIN02@%" in res):
               print("\nLogged in as Admin..")
          else:
               print("\nLogged in as Staff..")
          return db


def car_entered(db,mycursor):
     reg_no=input("Please Enter the car Registration number : ")
     str1=f"select * from vehicle_Details where Registration_number= '{reg_no}'"
     mycursor.execute(str1)
     res1=mycursor.fetchone()
     if(res1):      #if car is present in database
          print("Car is present in database")
          car_present(db,mycursor,reg_no)
     # else:        #if car is not present in database
          # print("Car is present in database")
     #      car_notpresent(db,mycursor,reg_no)

def car_present(db,mycursor,reg_no):
     check_flg=f"Select check_flag from vehicle_details where Registration_Number = '{reg_no}'"
     mycursor.execute(check_flg)
     check_flg=mycursor.fetchone()[0]
     if (check_flg!=1 and check_flg!=0):
          print("This is a government vehicle and is exempted from tax..")
          return
     toll_no=int(input(("Please enter the toll booth number where the vehicle entered [less than 4] ")))
     while(toll_no>4):
          print("Entered Toll Booth ID does not exist\n Please enter valid Toll Booth number : ")
          toll_no=int(input(("Please enter the toll booth number where the vehicle entered [less than 4] ")))
     balanc=f"select distinct balance from Transaction_Details natural join Vehicle_Details natural join Account_Details where Vehicle_Details.Registration_Number='{reg_no}'"
     mycursor.execute(balanc)      #get balance 
     balanc=mycursor.fetchone()[0]
     print("Balance : ",balanc)
     faree=f"select Toll_Price from Fare_Table natural join Vehicle_Details where Vehicle_Details.Registration_Number='{reg_no}'"
     mycursor.execute(faree)       #get toll price
     faree=mycursor.fetchone()[0]
     print("Amount to be deducted : ",faree)
     print(check_flg)
     if(check_flg==0):   #balance is less than fare
          print("Your account balance is low..")
          print("Please recharge now.")
          recharg=0
          recharg=int(input(f"Enter the recharge amount (Minimum amount : {faree}). "))
          while(recharg<faree):
               print("Please enter minimum amount")
               recharg=int(input(f"Enter the recharge amount (Minimum amount : {faree}). "))
          balanc+=recharg-faree
          update_balanc=f"UPDATE Account_Details natural JOIN Transaction_Details SET Account_Details.balance = {balanc} WHERE Transaction_Details.Registration_Number = '{reg_no}'"
          mycursor.execute(update_balanc)       #update the balance 
          db.commit()
          print("Recharge successful..")
          print("Tax deducted sucessfully..\n Balance amount has been updated")
          print("Balance amount : ",balanc)
     else:          #customer has enough balance
          balanc-=faree
          update_balanc=f"UPDATE Account_Details natural JOIN Transaction_Details SET Account_Details.balance = {balanc} WHERE Transaction_Details.Registration_Number = '{reg_no}'"
          mycursor.execute(update_balanc)       #update the balance 
          db.commit()
          print("Tax deducted successfully..")
          print("Remaining balance : ",balanc)
          ch=input("Would you like to recharge now? [Y/N]")
          recharg=0

          if (ch in ['Y','y']):         
               recharg=int(input("Enter the recharge amount(Recommended if Balance is less than Tax): "))
               if (recharg<0):
                    print("Invalid amount")
               balanc+=recharg
               new_balance=f"UPDATE Account_Details natural JOIN Transaction_Details SET Account_Details.balance = {balanc} WHERE Transaction_Details.Registration_Number = '{reg_no}'"
               mycursor.execute(new_balance)       #update the balance 
               db.commit()
               print("Recharge successful..")
               print("New balance : ",balanc)

     if (balanc>faree):          #check if newbalance is not low
          str4=f"Update Vehicle_Details set check_flag=1 where registration_number='{reg_no}'"
          mycursor.execute(str4)
          db.commit()
     else:
          str4=f"Update Vehicle_Details set check_flag=0 where registration_number='{reg_no}'"
          mycursor.execute(str4)
          db.commit()
          print("Check bit updated.")
     str5=f"Select toll_revenue from Toll_Booth where Toll_Booth_No={toll_no}"
     mycursor.execute(str5)
     toll_revn=mycursor.fetchone()[0]
     toll_revn+=faree+recharg
     str6=f"update Toll_Booth set Toll_Revenue={toll_revn} where Toll_Booth_No = {toll_no}"
     mycursor.execute(str6)
     db.commit()
     print("Toll Booth Revenue updated.")
     print(f"Total revenue collected for {toll_no} toll booth: {toll_revn}")
     return


     

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


              
