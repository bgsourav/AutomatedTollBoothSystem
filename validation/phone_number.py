import re
from pprint import pprint
import inquirer  

#Begins with 6,7,8 or 9 followed by 9 digits
def phone_validation(answers, current):
    if not re.match("[6-9][0-9]{9}$", current):
        raise inquirer.errors.ValidationError("", reason="Invalid phone number format!")
    return True

questions = [
    inquirer.Text("phone",message="Enter phone number",validate=phone_validation)
]
answers = inquirer.prompt(questions)
pprint(answers)