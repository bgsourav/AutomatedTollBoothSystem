from features import *
global global_usercount
global_usercount=3
print("\nWelcome to ATM\n")
print("<Fare details here..>")
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
