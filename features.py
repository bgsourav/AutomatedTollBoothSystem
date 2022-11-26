
import mysql.connector
from bullet import Password
def login():
    usernm = input("Enter username (Minimum length is 4): ")
    cli = Password(prompt = "Enter password: ",hidden="*")
    passwd = cli.launch()
    flag = 0
    try:
        if (usernm != "root" and len(usernm) > 3 and passwd):  # must not login as root
            db = mysql.connector.connect(host="localhost",
                                         user=usernm,
                                         password=passwd,
                                         db="tollboothmanagementsystem")
            cursor = db.cursor()
            flag = 1
        else:
            print("\nEither USERNAME does not exists or invalid PASSWORD Login failed!\n")
    except mysql.connector.Error as e:
        print("Error occured: " ,e)
        print("\nCredentials do not match\n")
        return
    if (flag):
        str1 = 'select current_user()'  # gives the name of the loged in account
        cursor.execute(str1)
        res = cursor.fetchone()
        logn=f"Select distinct user_type from user where user_name like 'ADMIN%'"
        cursor.execute(logn)
        logn=cursor.fetchone()[0]
        if(logn==1):
            print("\nLogged in as Admin..")
        else:
            print("\nLogged in as Staff..")
        return db

def create_staff(db,cursor,global_usercount):
    staff_name = input("Please enter the name of the Staff:")
    cli = Password(prompt = "Enter the associated password for {} - >".format(staff_name),hidden="*")
    staff_password = cli.launch()
    try:
        cursor.execute(f"create user '{staff_name}'@'localhost' identified by '{staff_password}';")
    except:
        #Error has occurred
        print("Error has occurred!")
        print("Please try again...")
        #sending control flow back for reexecution so that the process continues
        create_staff(db,cursor,global_usercount)
        return
    #No error during execution
    #Send in a global count to let me know how many users are there
    global_usercount = global_usercount + 1
    #tables for which staff need access
    tables_for_staff = ["Transaction_Details","Access","Uses","Vehicle_Details","Account_Details"]
    for i in tables_for_staff:
        cursor.execute(f"grant create on TollBoothManagementSystem.{i} to '{staff_name}'@'localhost';")
    #inserting the new staff to the Toll_Booth table
    cursor.execute(f"insert into Toll_Booth values ({global_usercount},'{staff_name}',0)")
    cursor.execute(f"grant update on TollBoothManagementSystem.Toll_Booth to user{staff_name};")


def transac_id(db,mycursor,acc_no,phone_no,reg_no):
    print("sdfdf",acc_no,phone_no,reg_no)
    flag=1
    while(flag):
        trid = input("Enter the Transaction Id [format TRXXXXXX]: ")
        str1="Select Transaction_ID from Transaction_Details"
        mycursor.execute(str1)
        str1=mycursor.fetchall()
        print(str1)
        att=[i[0] for i in str1]
        if(trid in att):
            print("Error occured: ")
            print("Please try again..")
        else:
            flag=0
    ins3 = f"INSERT INTO Transaction_Details values ('{trid}',{acc_no},{phone_no},'{reg_no}')"
    mycursor.execute(ins3)            
    #db.commit()

    
    
def car_entered(db, mycursor):
    reg_no = input("Please Enter the Vehicle Registration number : ")
    str1 = f"select * from vehicle_Details where Registration_number= '{reg_no}'"
    mycursor.execute(str1)
    res1 = mycursor.fetchone()
    if (res1):  # if car is present in database
        print("Vehicle is present in database")
        car_present(db, mycursor, reg_no)
    # else:        #if car is not present in database
        # print("Vehicle is not present in database.\nPlease register.")
    #      car_notpresent(db,mycursor,reg_no)


def car_present(db, mycursor, reg_no):
    check_flg = f"Select check_flag from vehicle_details where Registration_Number = '{reg_no}'"
    mycursor.execute(check_flg)
    check_flg = mycursor.fetchone()[0]
    if (check_flg != 1 and check_flg != 0):
        print("This is a government vehicle and is exempted from tax..")
        return
    toll_no = int(input(
        ("Please enter the toll booth number where the vehicle entered [less than 4] ")))
    while (toll_no > 4):
        print(
            "Entered Toll Booth ID does not exist\n Please enter valid Toll Booth number : ")
        toll_no = int(input(
            ("Please enter the toll booth number where the vehicle entered [less than 4] ")))
    balanc = f"select distinct balance from Transaction_Details natural join Vehicle_Details natural join Account_Details where Vehicle_Details.Registration_Number='{reg_no}'"
    mycursor.execute(balanc)  # get balance
    balanc = mycursor.fetchone()[0]
    print("Balance : ", balanc)
    faree = f"select Toll_Price from Fare_Table natural join Vehicle_Details where Vehicle_Details.Registration_Number='{reg_no}'"
    mycursor.execute(faree)  # get toll price
    faree = mycursor.fetchone()[0]
    acc_no=f"Select distinct Account_Number,Phone_Number from Transaction_Details where Registration_Number='{reg_no} group by Account_Number'"
    mycursor.execute(acc_no)  # get account number and phone number
    arr1=mycursor.fetchall()
    acc_no=[i[0] for i in arr1]
    phonm=[i[1] for i in arr1]
    print("Account and Phone number available to recharge: \n")
    print("Choice\t Account number\t Phone number")
    for i in range(len(acc_no)):
        print(f" {i+1}> \t{acc_no[i]} \t{phonm[i]}. \n")
    numb=int(input("Enter your choice ?  "))
    while (numb> len(phonm) or numb<1):
        numb=int(input("Please Enter a valid choice: "))
    numb-=1
    print("Phone number chosen: ",phonm[numb])
    print("Amount to be deducted : ", faree)
#     print(check_flg)
    if (check_flg == 0):  # balance is less than fare
        recharg, balanc = low_balance(db, mycursor, faree, balanc, reg_no,acc_no[numb],phonm[numb])

    else:  # customer has enough balance
        recharg, balanc = enough_balance(db, mycursor, faree, balanc, reg_no,acc_no[numb],phonm[numb])

    update_chkbit(db,mycursor,balanc,faree,reg_no)
    
    str5 = f"Select toll_revenue from Toll_Booth where Toll_Booth_No={toll_no}"
    mycursor.execute(str5)
    toll_revn = mycursor.fetchone()[0]
    toll_revn += faree
    str6 = f"update Toll_Booth set Toll_Revenue={toll_revn} where Toll_Booth_No = {toll_no}"
    mycursor.execute(str6)
    db.commit()
    print("Toll Booth Revenue updated.")
    print(f"Total revenue collected for {toll_no} toll booth: {toll_revn}")
    return

def low_balance(db, mycursor, faree, balanc, reg_no,acc_no,phone_no):
    print("Your account balance is low..")
    print("Please recharge now.")
    recharg = 0
    recharg = int(
        input(f"Enter the recharge amount (Minimum amount : {faree-balanc}). "))
    while (recharg < faree-balanc):
        print("Please enter minimum amount")
        recharg = int(
            input(f"Enter the recharge amount (Minimum amount : {faree-balanc}). "))
    balanc += recharg-faree
    transac_id(db,mycursor,acc_no,phone_no,reg_no)
    update_balanc = f"UPDATE Account_Details natural JOIN Transaction_Details SET Account_Details.balance = {balanc} WHERE Transaction_Details.Registration_Number = '{reg_no}'"
    mycursor.execute(update_balanc)  # update the balance
    db.commit()
    print("Recharge successful..")
    print("Tax deducted sucessfully..\n Balance amount has been updated")
    print("Balance amount : ", balanc)
    return [recharg, balanc]


def enough_balance(db, mycursor, faree, balanc, reg_no,acc_no,phone_no):
    balanc -= faree
    update_balanc = f"UPDATE Account_Details natural JOIN Transaction_Details SET Account_Details.balance = {balanc} WHERE Transaction_Details.Registration_Number = '{reg_no}'"
    mycursor.execute(update_balanc)  # update the balance
    db.commit()
    print("Tax deducted successfully..")
    print("Remaining balance : ", balanc)
    transac_id(db,mycursor,acc_no,phone_no,reg_no)
    ch = input("Would you like to recharge now? [Y/N]")
    recharg = 0

    if (ch in ['Y', 'y']):
        recharg = int(
            input("Enter the recharge amount(Recommended if Balance is less than Tax): "))
        if (recharg < 0):
            print("Invalid amount")
        balanc += recharg
        new_balance = f"UPDATE Account_Details natural JOIN Transaction_Details SET Account_Details.balance = {balanc} WHERE Transaction_Details.Registration_Number = '{reg_no}'"
        mycursor.execute(new_balance)  # update the balance
        print("Recharge successful..")
        print("New balance : ", balanc)
        transac_id(db,mycursor,acc_no,phone_no,reg_no)
        db.commit()
    return [recharg, balanc]

def update_chkbit(db,mycursor,balanc,faree,reg_no):
     if (balanc > faree):  # check if newbalance is not low
        update_checkbit = f"Update Vehicle_Details set check_flag=1 where registration_number='{reg_no}'"
        mycursor.execute(update_checkbit)
        db.commit()
     else:
        update_checkbit = f"Update Vehicle_Details set check_flag=0 where registration_number='{reg_no}'"
        mycursor.execute(update_checkbit)
        db.commit()
        print("Check bit updated.")

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
