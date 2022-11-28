from features import *
from prettytable import PrettyTable
import inquirer
from simple_chalk import chalk,green,red,yellowBright,redBright,greenBright,blueBright,cyan
global global_usercount
global_usercount=4
def run():
     print(yellowBright.bold("\nWelcome to Automated Toll Booth Machine\n"))
     print(cyan("Fare details here.."))
     print("")
     # Custom_table = cus_tab
     cus_tab = PrettyTable()
     cus_tab.field_names = ["Vehicle_Type","Toll_Price"]
     cus_tab.add_row(["Four_axle_truck",150])
     cus_tab.add_row(["Short_vehicle",50])
     cus_tab.add_row(["Three_axle_truck",100])
     cus_tab.add_row(["Two_axle_truck",75])
     cus_tab.sortby = 'Toll_Price'
     print(cus_tab)
     while True:
          ch=input(blueBright("Do you want to login? [Y/N]\n")) #Simple_chalk functions can be nested with '.' and are callable like a function
          while(ch in ['y','Y']):
               is_admin = 0
               res = login()
               db = None
               if(res != None):
                    db = res[0]
                    is_admin = res[1]
               while(db):
                    cursor = db.cursor(buffered = True)
                    print("\n")
                    if is_admin == 1:
                         operations = [
                              inquirer.List('op_x',
                              message = "Which Operation would you like to perform?",
                              choices = ['1.)Create New User','2.)Enter Car Details','3.)Exit'],
                              ),
                         ]
                    elif is_admin == 0:
                         operations = [
                              inquirer.List('op_x',
                              message = "Which Operation would you like to perform?",
                              choices = ['1.)Enter Car Details','2.)Exit'],carousel = True
                              ),
                         ]
                    answer = inquirer.prompt(operations)['op_x']
                    #'op_x' refers to the operation of which the answer is of
                    #the inquirer prompt returns a Dicitonary which is of the form
                    #{'op_x':Choice}
                    if(answer in ['1.)Enter Car Details','2.)Enter Car Details']):
                         car_entered(db,cursor)
                    elif("Create New User" in answer):
                         create_staff(db,cursor,global_usercount)
                    else:
                         ch1=input("Are you sure you want to Log Out?[Y/N] ")
                         if(ch1 in ['y','Y']):
                              ch='n'
                              break
               if (ch in ['Y','y']):
                    ch=input("Would you like to try again? [Y/N]\n")
          if (ch in ['N','n']) :
               print("Ok. Thank You!")
               break
          else:
               print("Please enter a valid choice")
               print("")
if __name__ == "__main__":
     run()
