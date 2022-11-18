from features import *
from prettytable import PrettyTable
global global_usercount
global_usercount=3
print("\nWelcome to ATM\n")
print("Fare details here..")
print("")
cus_tab = PrettyTable()
cus_tab.field_names = ["Vehicle_Type","Toll_Price"]
cus_tab.add_row(["Four_axle_truck",150])
cus_tab.add_row(["Short_vehicle",50])
cus_tab.add_row(["Three_axle_truck",100])
cus_tab.add_row(["Two_axle_truck",75])
print(cus_tab)
print("")
ch=input("Do you want to login? [Y/N]\n")
while(ch in ['y','Y']):
     db= login()
     while(db ):
          cursor=db.cursor()
          # car_entered(db,cursor)
          print("Adding staff")
          create_staff(db,cursor,global_usercount)
          ch1=input("Would you like to logout?[Y/N] ")
          if(ch1 in ['y','Y']):
               ch='n'
               break
     if (ch in ['Y','y']):
          ch=input("Would you like to try again? [Y/N]\n")
if (ch in ['N','n']) :
     print("Ok. Thank You!")
else:
     print("Please enter a valid choice")
