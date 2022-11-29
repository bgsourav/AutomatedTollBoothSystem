import re
from pprint import pprint
import inquirer  

#ADM OR USR followed by three numbers
print('User Name must be User Type(ADM/USR) followed by three numbers')

def username_validation(answers, current):
    if not re.match("[U][S][R][0-9]{2}[1-9]$", current):
        raise inquirer.errors.ValidationError("", reason="Invalid user name format!")
    if not re.match("[A][D][M][0-9]{2}[1-9]$",current):
        raise inquirer.errors.ValidationError("", reason="Invalid user name format!")
    return True


questions = [
    inquirer.Text("User Name",message="Enter user name",validate=username_validation)
]
answers = inquirer.prompt(questions)
pprint(answers)
