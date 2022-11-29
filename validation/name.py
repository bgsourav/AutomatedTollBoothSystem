import re
from pprint import pprint
import inquirer  

def name_validation(answers, current):
    if not re.match("^[A-Z][a-z]+\s[A-Z][a-z]+$",current):
        raise inquirer.errors.ValidationError("", reason="Check for invalid numeric or special character inputs!")
    return True

questions = [
    inquirer.Text("Name",message="Enter name",validate=name_validation)
]
answers = inquirer.prompt(questions)
pprint(answers)