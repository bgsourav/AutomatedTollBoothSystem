import re
from pprint import pprint
import inquirer  

#Minimum eight characters, at least one letter and one number
print('Password must be between 8 to 16 characters long with at least one letter and a number')

def password_validation(answers, current):
    if not re.match("^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,16}$", current):
        raise inquirer.errors.ValidationError("", reason="Password condition not satisfied!")
    return True

questions = [
    inquirer.Text("Password",message="Enter Password",validate=password_validation)
]
answers = inquirer.prompt(questions)
pprint(answers)