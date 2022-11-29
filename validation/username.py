import re
from pprint import pprint
import inquirer  

#ADM OR USR followed by three numbers
print('User Name must be User Type(ADM/USR) followed by three numbers')

def username_validation(answers, current):
    if not re.match("STF[0-9]{2}[1-9]$|ADM[0-9]{2}[1-9]$", current):
        raise inquirer.errors.ValidationError("", reason="Invalid user name format!")
    return True


questions = [
    inquirer.Text("User Name",message="Enter user name",validate=username_validation)
]
answers = inquirer.prompt(questions)
pprint(answers)
