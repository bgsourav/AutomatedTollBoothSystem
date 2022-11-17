from features import *

print("\nWelcome to ATM\n")
print("<Fare details here..>")
ch=input("Do you want to login? [Y/N]\n")
while(ch in ['y','Y']):
     db= login()
     if(db):
          cursor=db.cursor()
          car_entered(db,cursor)
     else:
          ch=input("Would you like to try again? [Y/N]\n")
if (ch in ['N','n']) :
     print("Ok. Thank You!")
