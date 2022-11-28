import mysql.connector
import maskpass
from simple_chalk import chalk,green,red,yellowBright,redBright,greenBright
def login():
    usernm = input("Enter username (Minimum length is 4): ")
    passwd= maskpass.askpass()
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
            print(redBright.bold.underline("\nEither USERNAME does not exists or invalid PASSWORD.\nLogin failed!\n"))
    except mysql.connector.Error as e:
        print(redBright.bold.underline("Error occured: {}\n".format(e)))
        print(redBright.bold.underline("\nCredentials do not match\n"))
        return
    if (flag):
        str1 = 'select current_user()'  # gives the name of the loged in account
        cursor.execute(str1)
        res = cursor.fetchone()
        logn=f"Select distinct user_type from user where user_name like 'ADMIN%'"
        cursor.execute(logn)
        logn=cursor.fetchone()[0]
        print(res)
        if(logn==1):
            print(greenBright.bold.underline("\nLogged in as Admin..\n"))
        else:
            print(greenBright.bold.underline("\nLogged in as Staff..\n"))
        return db,logn

def create_staff(db,cursor,global_usercount):
    staff_name = input("Please enter the name of the Staff:")
    cli = Password(prompt = "Enter the associated password for {} - >".format(staff_name),hidden="*")
    staff_password = cli.launch()
    try:
        cursor.execute(f"create user '{staff_name}'@'localhost' identified by '{staff_password}';")
    except mysql.connector.Error as e:
        #Error has occurred
        print("Error has occurred!")
        print("Please try again...")
        print(e.body)
        #sending control flow back for reexecution so that the process continues
        create_staff(db,cursor,global_usercount)
        return
    #No error during execution
    #Send in a global count to let me know how many users are there
    cursor.execute(f"select COUNT(*) from Toll_Booth;")
    tempo = cursor.fetchone()[0]
    print(tempo)
    global_usercount = global_usercount + 1
    #tables for which staff need access
    tables_for_staff = ["Transaction_Details","Access","Uses","Vehicle_Details","Account_Details"]
    for i in tables_for_staff:
        cursor.execute(f"grant create on TollBoothManagementSystem.{i} to '{staff_name}'@'localhost';")
    #inserting the new staff to the Toll_Booth table
    cursor.execute(f"insert into Toll_Booth values ({global_usercount},'{staff_name}',0)")
    cursor.execute(f"grant update on TollBoothManagementSystem.Toll_Booth to user{staff_name};")


def transac_id(db,mycursor,acc_no,phone_no,reg_no):
    #print("sdfdf",acc_no,phone_no,reg_no)
    flag=1
    while(flag):
        trid = input("Enter the Transaction Id [format TRXXXXXX]: ")
        str1="Select Transaction_ID from Transaction_Details"
        mycursor.execute(str1)
        str1=mycursor.fetchall()
        # print(str1)
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
    else:        #if car is not present in database
        print("Vehicle is not present in database.\nPlease register.")
        car_notpresent(db,mycursor,reg_no)

def car_present(db, mycursor, reg_no):
    try:
        mycursor.execute(f"select COUNT(*) from Toll_Booth;")
        tempo = mycursor.fetchone()[0]
        toll_no = int(input(
            (f"Please enter the toll booth number where the vehicle entered [less than {tempo}] ")))
        while (toll_no > tempo):
            print(
                "Entered Toll Booth ID does not exist\n Please enter valid Toll Booth number : ")
            toll_no = int(input(
                ("Please enter the toll booth number where the vehicle entered [less than 4] ")))
        check_flg = f"Select check_flag from vehicle_details where Registration_Number = '{reg_no}'"
        mycursor.execute(check_flg)
        check_flg = mycursor.fetchone()[0]
        if (check_flg != 1 and check_flg != 0):
            print("This is a government vehicle and is exempted from tax..")
            mycursor.execute(f"insert into access values ('{reg_no}',{toll_no}, CURRENT_TIMESTAMP()) ")
            db.commit()
            return
        faree = f"select Toll_Price from Fare_Table natural join Vehicle_Details where Vehicle_Details.Registration_Number='{reg_no}'"
        mycursor.execute(faree)  # get toll price
        faree = mycursor.fetchone()[0]
        print("Fare : ", faree)
        ch2=input("Would you like to register another account?[Y/N] ")
        while(ch2 in ['Y','y']):
            ret=register_account(db,mycursor,reg_no,faree)
            if(ret==0):
                ch2=input("Would you like to register another account?[Y/N] ")
            else:
                break
        acc_no=f"Select distinct Account_Number,Phone_Number from Transaction_Details where Registration_Number='{reg_no}' group by Account_Number"
        mycursor.execute(acc_no)  # get account number and phone number
        arr1=mycursor.fetchall()
        acc_no=[i[0] for i in arr1]
        phonm=[i[1] for i in arr1]
        print("Account and Phone number available to recharge: \n")
        print("Choice\t Account number\t Phone number")
        for i in range(len(acc_no)):
            print(f" {i+1}> \t {acc_no[i]} \t {phonm[i]}. \n")
        numb=int(input("Enter your choice ?  "))
        while (numb> len(phonm) or numb<1):
            numb=int(input("Please Enter a valid choice: "))
        numb-=1
        print("Account number chosen: ",acc_no[numb])
        print("Amount to be deducted : ", faree)
        balanc = f"select distinct balance from Transaction_Details natural join Vehicle_Details natural join Account_Details where Vehicle_Details.Registration_Number='{reg_no}' and Account_Details.Account_Number={acc_no[numb]}"
        mycursor.execute(balanc)  # get balance
        balanc = mycursor.fetchone()[0]
        print("Balance : ", balanc)
        if (balanc<faree):      # balance is low
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
        mycursor.execute(f"insert into access values ('{reg_no}',{toll_no}, CURRENT_TIMESTAMP()) ")
        db.commit()
        print("Toll Booth Revenue updated.")
        print(f"Total revenue collected for {toll_no} toll booth: {toll_revn}")
        return
    except mysql.connector.Error as e:
        print("\nError has Occured!!.. i.e : ",e

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
    update_balanc = f"UPDATE Account_Details natural JOIN Transaction_Details SET Account_Details.balance = {balanc} WHERE Transaction_Details.Registration_Number = '{reg_no}' and Account_Details.Account_Number={acc_no}"
    mycursor.execute(update_balanc)  # update the balance
    db.commit()
    print("Recharge successful..")
    print("Tax deducted sucessfully..\n Balance amount has been updated")
    print("Balance amount : ", balanc)
    return [recharg, balanc]


def enough_balance(db, mycursor, faree, balanc, reg_no,acc_no,phone_no):
    balanc -= faree
    update_balanc = f"UPDATE Account_Details natural JOIN Transaction_Details SET Account_Details.balance = {balanc} WHERE Transaction_Details.Registration_Number = '{reg_no}' and Account_Details.Account_Number={acc_no}"
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
        new_balance = f"UPDATE Account_Details natural JOIN Transaction_Details SET Account_Details.balance = {balanc} WHERE Transaction_Details.Registration_Number = '{reg_no}' and Account_Details.Account_Number={acc_no}"
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


def car_notpresent(db, mycursor, reg_no):
    print("Enter the Check flag i.e. the designation of the Vehicle: \n")
    cf = int(input("Type \n 2 - Government Vehicle \n 1 - Not a Government Vehicle :- \n")) 
    #print("Check flag = ",cf,"\n")
    print("Enter the type of the Vehicle: \n")
    while(1):
        vt = input("Type \n 4 - Four Axle Truck \n 3 - Three Axle Truck \n 2 - Two Axle Truck \n 1 - Short Vehicle :- \n")
        if vt == '4':
            Vehicle_Type = "Four_axle_truck"
            fare = 150
            break
        elif vt == '3':
            Vehicle_Type = "Three_axle_truck"
            fare = 100
            break
        elif vt == '2':
            Vehicle_Type = "Two_axle_truck"
            fare = 75
            break
        elif vt == '1':
            Vehicle_Type = "Short_vehicle"
            fare = 50
            break
        else:
            print("\nPlease Enter the correct option..\n")
    print("You have chosen Vehicle Type as - " + Vehicle_Type)
    try:
        ins1 = f"INSERT INTO Vehicle_Details values (%s, %s, %s);"
        st1 = (cf, Vehicle_Type, reg_no) 
        mycursor.execute(ins1, st1)
        db.commit()
        if cf == 2:
            print("\nThis is a government vehicle and is exempted from tax..\n")
            return
        register_account(db,mycursor,reg_no,fare)
        car_present(db, mycursor, reg_no)
    except mysql.connector.Error as e:
        print("\nError has Occured!!.. i.e : ",e)
        db.rollback()
        return
    print("")


def register_account(db,mycursor,reg_no,fare):
    try:
        fname = input("Enter your First Name: ")
        lname = input("Enter your Last Name: ")
        accno = int(input("Enter your Account Number: "))
        bal = 0
        cf=1
        while(cf == 1):
            bal = int(input("Enter the Balance in your account: "))
            if bal < fare:
                # cf = 0
                print("\nNot sufficient balance!!\nTry again..\n")
            else:
                #bal = bal - fare
                #cf = 1
                break
        ins2 = f"INSERT INTO Account_Details values (%s, %s, %s, %s);"
        st2 = (accno, fname, lname, bal)
        mycursor.execute(ins2, st2)
        trid = input("Enter the Transaction Id for recharge: ")
        phno = int(input("Enter your Phone Number: "))
        ins3 = f"INSERT INTO Transaction_Details values (%s, %s, %s, %s);"
        st3 = (trid, accno, phno, reg_no)
        mycursor.execute(ins3, st3)
        db.commit()
        print("Successfully recharged..")
        return 1
    except mysql.connector.Error as e:
        print("\nError has Occured!!.. i.e : ",e)
        db.rollback()
        return 0
